# 3D Sudoku Solver

This is a **backtracking solver for a 3D Sudoku puzzle** - imagine a Rubik's cube where you need to arrange 27 numbered dice so that each face of the 3×3×3 structure shows the digits 1-9 exactly once.

## The Problem

You have 27 small cubes, each with numbers on some faces (or blanks). You need to:
- Place all 27 cubes into a 3×3×3 grid
- Ensure each of the 6 outer faces shows digits 1-9 with no repeats

<img src="images/cube.jpeg" alt="The 3x3x3 puzzle" width="60%">

Note that blank faces of the cubes are hidden on the inside. In other words, there is an exact number of marked, visible faces. There's:

* one entirely blank cube that is always in the middle
* six centre-face cubes, each with one number marked
* twelve "edge" cubes, with two numbers
* eight "corner" cubes, with three numbers

6s and 9s are not distinguished on the faces. The solver therefore needs to treat 6 and 9 as alternates.

That allows us to see that:
* only certain cubes will fit in a given slot in the grid
* only certain orientations will fit.

We choose a [convention](prototype/marks.py) for numbering the sides of the cube (and the board), and for the number of non-blank faces.

That allows for a simple declaration of the specific [pieces](prototype/3dsudoku.py) in play.

Each of the 24 different rotations, and the 6/9 variants can be easily done [here](prototype/define_cube.py).

## Algorithm

Finding _a_ solution was relatively quick and easy with Python, for example:

```
- 1 3 - - 1 | - 3 - - - 2 | - 7 - 3 - 5 |
- 9 1 - - - | - 4 - - - - | - 5 - 7 - - |
- 2 4 - 2 - | - 8 - - 4 - | - 6 - 5 8 - |

- - 5 - - 4 | - - - - - 3 | - - - 6 - 7 |
- - 7 - - - | - - - - - - | - - - 8 - - |
- - 9 - 5 - | - - - - 9 - | - - - 9 3 - |

1 - 8 - - 8 | 5 - - - - 6 | 3 - - 1 - 9 |
7 - 6 - - - | 8 - - - - - | 6 - - 4 - - |
2 - 2 - 6 - | 4 - - - 7 - | 9 - - 2 1 - |
```

This shows bottom, middle, and top layers. Each cube's faces (e.g. `- 1 3 - - 1`) show in the conventional order of
_top, bottom, left, right, front, back_.

This leads to: how many distinct solutions are there? To find all solutions, use a classic **backtracking search**:

```
For each position in the 3×3×3 grid:
  For each available cube that could fit here:
    For each valid rotation of that cube:
      If it doesn't create duplicate numbers on any face:
        ✓ Place the cube
        ✓ Recursively solve the rest
        ✓ Remove the cube (backtrack)
```

The solver gets the first answer in a fraction of a second. At first I thought there might be a few thousand, or a few million valid solutions that could be found with reasonable runtime. There are many more than that!

## [Prototype](prototype) implementation

Data structures and algorithms were initially built in Python, allowing various algorithm choices to be easily explored.

1. **Pre-filtering** - The `SlotVariants` structure means we only try cubes that:
   - Have the right number of visible faces for that position (corner=3, edge=2, face=1, center=0)
   - Have no blanks on visible faces

1. **Exploit symmetry** - Force the first corner cube to always be a specific choice. After all, the solved "big" cube has full rotational symmetry. This reduces redundant searches by ~24×.

    > If you want to consider each big cube orientation as unique, just multiply the already huge number of solutions by 24.

1. **Early termination** - The `is_valid2()` check immediately rejects placements that would create duplicate numbers

1. **Two solve functions** - `solve_from_pos()` prints progress for the first 8 positions, `solve_from_pos_deep()` runs silently for deeper recursion (avoiding I/O overhead in the tight inner loop)

1. **Linear recursion over positions** - While the puzzle is conceptually a 3×3×3 grid, the solver recurses over a flattened 27-element array (`strip`). The traversal order is z→y→x (so position 0 is grid[0][0][0], position 1 is grid[1][0][0], etc.). This provides better cache locality and simpler indexing (single integer position instead of x,y,z coordinates), making the inner loop faster.

## Need for speed

The next optimization was to use [pypy](https://pypy.org/index.html) instead of the usual Python3 interpreter. This gave ~3x speedup.

## Rust

In late 2024, ChatGPT helped me translate the code into Rust. However, this gave about a ~2.5x compared to pypy, probably because I was fighting against the borrow-checker and didn't apply the right optimizations. The Rust version still used hash-based sets rather than bitmasks.

## C++

The problem space fits perfectly into bitmask operations, instead of hash-based sets. 64 bits easily handles both 10 digits and 27 cubes.
In late 2025, CoPilot (Claude Sonnet 4.5) helped translate the Python into C++ with this optimization.

**Bitmasks (uint64_t)** - The key speedup over Python
- Instead of Python sets, uses binary bits to track which numbers/cubes are used
- `sides[6]`: 6 bitmasks tracking which digits appear on each face (each storing 10 bits for digits 0-9)
- `available`: bitmask of which cubes haven't been placed yet (27 bits for cube IDs 0-26)
- Operations like "is 7 already on the top face?" become single CPU-level bitwise operations
- Uses CPU intrinsics (`__builtin_ctzll` for finding first set bit, `__builtin_popcountll` for counting bits) that map directly to hardware instructions
- Much faster than Python set operations due to no hashing overhead and better cache locality

**Additional C++ optimizations:**
- Branch prediction hints (`[[likely]]` attributes) guide the compiler to optimize the most common code paths
- Inline functions eliminate function call overhead in hot loops

The pre-computed variants, state tracking, and other algorithmic optimizations remain the same as the Python prototype.

The result is an optimized constraint satisfaction solver that can explore millions of placements per second.

### Build instructions
I found `clang++` to be slightly faster than `g++` on both Apple M3 (ARM) and Linux/x64 architectures. This works for both:

```bash
clang++ -O3 -march=native -funroll-loops -fomit-frame-pointer -ffast-math -o 3dsudoku 3dsudoku.cpp
```

## Parallelization Strategy

The solver itself is single-threaded and will saturate a single core. However, to exploit modern multi-core CPUs (and even distribute work across multiple machines), the solver accepts a command-line argument specifying which cube to place at _position 1_ (an edge piece).

Note: Position 0 (grid[0][0][0], a corner) is automatically fixed to break symmetry. Position 1 (grid[1][0][0], an edge) is where we can inject different cubes to partition the problem space.

```bash
./3dsudoku 8   # Force cube #8 at position 1
```

This allows you to divide the problem space across cores or machines by running multiple instances with different hint cube IDs. ID 7 is invalid (the 1s clash) so we only need to try edge piece IDs 8-18. This needs 11 processes.
Each process explores an independent subtree of the search space. The results can be written to different .txt files, see [do_all.sh](do_all.sh).

The results can be summed to get the total solution count.

Each process can be tuned after starting, with `renice` so that, for example, seven processes run with normal priority on seven cores, while the remaining 4 run more slowly (to minimize context switching).

## Checking against Python code

The "Christmas 2024" Python run found ~ 65 billion solutions. A [comparison script](./compare_outputs.py) allows the new run to be checked against this (for cube 8).


```bash
 ./compare_outputs.py out.txt ./out-cube8.txt
Comparing out.txt vs ./out-cube8.txt
Showing lines with dashcount <= 4
======================================================================
out.txt: 475956 lines
./out-cube8.txt: 244245 lines

Note: Different number of lines - comparing up to shorter length

✓ ---- with - 4 - - - - 427,123,712 solutions | ---- with - 4 - - - - 427,123,712 solutions | 5.69x
✓ ---- with - 8 - - - - 832,529,920 solutions | ---- with - 8 - - - - 832,529,920 solutions | 6.21x
:
: etc
:
======================================================================
✓ No differences found! Outputs match.
```

This shows we haven't broken the C++ version.

## Estimating run-time

The [spreadsheet](estimating/combinations%20of%20first%20layer.xlsx) catalogues various runs done. On a 6th-gen Intel x64 machine running all 11 processes simultaneously, doing all variants of piece[2] is taking around two days. Extrapolating from this suggests the whole run will finish in about 160 days.