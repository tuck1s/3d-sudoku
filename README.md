# 3D Sudoku Solver

This is a **backtracking solver for a 3D Sudoku puzzle** - imagine a Rubik's cube where you need to arrange 27 numbered dice so that each face of the 3×3×3 structure shows the digits 1-9 exactly once.

## The Problem

You have 27 small cubes, each with numbers on some faces (or blanks). You need to:
- Place all 27 cubes into a 3×3×3 grid
- Ensure each of the 6 outer faces shows digits 1-9 with no repeats

<img src="images/cube.jpeg" alt="The 3x3x3 puzzle" width="60%">


## Algorithm

While finding _a_ solution was relatively quick and easy wih Python, this got me thinking: how many distinct solutions are there?

This became a "Christmas project" for 2024 and 2025 season.

To find all solutions, use a classic **backtracking search**:

```
For each position in the 3×3×3 grid:
  For each available cube that could fit here:
    For each valid rotation of that cube:
      If it doesn't create duplicate numbers on any face:
        ✓ Place the cube
        ✓ Recursively solve the rest
        ✓ Remove the cube (backtrack)
```

6s and 9s are not distinguished on the faces.
The solver therefore needs to treat 6 and 9 as alternates.

## [Prototype](prototype) implementation

Data structures and algorithms were initially built in Python, allowing various optimizations to be explored.

1. **Pre-filtering** - The `SlotVariants` structure means we only try cubes that:
   - Have the right number of visible faces for that position (corner=3, edge=2, face=1, center=0)
   - Have no blanks on visible faces

1. **Exploit symmetry** - Force the first corner cube to always be a specific choice. After all, the solved "big" cube has full rotational symmetry. This reduces redundant searches by ~24×.

    > If you want to consider each big cube orientation as unique, just multiply the already huge number of solutions by 24. 

1. **Early termination** - The `is_valid2()` check immediately rejects placements that would create duplicate numbers

1. **Two solve functions** - `solve_from_pos()` prints progress for shallow depths, `solve_from_pos_deep()` runs silently for deep recursion (avoiding I/O overhead in the tight loop)

## Need for speed

The next optimization was to use [pypy](https://pypy.org/index.html) instead of the usual Python3 interpreter. This gave ~3x speedup.

## Rust

In late 2024, I translated the Python into Rust with the help of ChatGPT. This gave only small speedup, probably because I'm a novice Rust programmer and was fighting against the borrow-checker.

## C++

In late 2025


## Key Data Structures

### 1. Bitmasks (uint64_t) 
- Instead of arrays/sets, uses binary bits to track which numbers/cubes are used
- `sides[6]`: 6 bitmasks tracking which digits appear on each face
- `available`: bitmask of which cubes haven't been placed yet
- Operations like "is 7 already on the top face?" become single bitwise operations (extremely fast)

### 2. Pre-computed Variants (`SlotVariants`)
- Before solving, calculates all 24 possible rotations of each cube
- Filters out invalid orientations (e.g., cubes with blank faces on visible sides)
- Stores only valid cube-orientation pairs for each position
- This means during search, we never try impossible placements

### 3. State
- Tracks current placement of all cubes
- Maintains which digits are visible on each of the 6 outer faces
- Updates incrementally as cubes are placed/removed

## Key Optimizations

1. **Bitmask operations** - All set membership checks are O(1) bitwise operations instead of O(n) loops

The result is a highly optimized constraint satisfaction solver that can explore millions of placements per second!
