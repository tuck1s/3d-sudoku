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

Finding _a_ solution was relatively quick and easy wih Python:

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

1. **Two solve functions** - `solve_from_pos()` prints progress for shallow depths, `solve_from_pos_deep()` runs silently for deep recursion (avoiding I/O overhead in the tight loop)

1. **Linear recursion over positions** - While the puzzle is conceptually a 3×3×3 grid, the solver recurses over a flattened 27-element array (`strip`). This provides better cache locality and simpler indexing (single integer position instead of x,y,z coordinates), making the inner loop faster.

## Need for speed

The next optimization was to use [pypy](https://pypy.org/index.html) instead of the usual Python3 interpreter. This gave ~3x speedup.

## Rust

In late 2024, I made an AI-assisted translation into Rust. This gave only small speedup compared to pypy, probably because I'm a novice Rust programmer and was fighting against the borrow-checker.

## C++

In late 2025, CoPilot (Claude Sonnet 4.5) helped translate the Python into C++, with a critical optimization:

**Bitmasks (uint64_t)** - The key speedup over Python
- Instead of Python sets, uses binary bits to track which numbers/cubes are used
- `sides[6]`: 6 bitmasks tracking which digits appear on each face
- `available`: bitmask of which cubes haven't been placed yet
- Operations like "is 7 already on the top face?" become single bitwise operations (extremely fast)
- All set membership checks are O(1) bitwise operations instead of O(n) hash table lookups

The pre-computed variants, state tracking, and other algorithmic optimizations remain the same as the Python prototype.

The result is a highly optimized constraint satisfaction solver that can explore millions of placements per second!
