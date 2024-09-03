#!/usr/bin/env python3

# Import the Cube class and the cubes list from the cubes_definition file
from define_cube import Cube, CubeCollection, Sides, Solutions
from typing import List, Set

# Define position checks for all six sides
def generate_checks(x: int, y: int, z: int, size: int) -> dict:
    return {
        Sides.left: x == 0,
        Sides.right: x == size - 1,
        Sides.front: y == size - 1,
        Sides.back: y == 0,
        Sides.top: z == size - 1,
        Sides.bottom: z == 0,
    }

def is_valid(sides:list, cube:Cube, x:int, y:int, z:int, size:int) -> bool:
    # print(f"Checking validity for cube at ({x}, {y}, {z}) with orientation {cube}")
    checks = generate_checks(x, y, z, size)
    # Iterate over all sides
    for side in Sides:
        if checks[side]:  # Check if the current side is on the border of the cube
            if cube[side] == 0 or (cube[side] in sides[side.value]):  # No repeating number on the same face
                return False
    return True

def update_sides(sides: List[Set[int]], cube: Cube, x: int, y: int, z: int, size: int):
    checks = generate_checks(x, y, z, size)
    for side in Sides:
        if checks[side]:
            sides[side.value].add(cube[side])

def remove_cube_from_sides(sides: List[Set[int]], cube: Cube, x: int, y: int, z: int, size: int):
    checks = generate_checks(x, y, z, size)
    for side in Sides:
        if checks[side]:
            sides[side.value].discard(cube[side])  # Use discard to avoid KeyError if the element is not present


def solve_sudoku_3d(board: list, sides: List[Set[int]], cubes: List[Cube], used: List[bool], idx: int, solutions:Solutions) -> bool:
    size = len(board)
    if idx == size * size * size:
        solutions.add(board)
        print(f'Solution #{len(solutions)}')
        print_board(board)
        return True  # All cubes placed

    # Iterate over all positions
    for x in range(size):
        for y in range(size):
            for z in range(size):
                if board[x][y][z] is None:  # Check for empty spot
                    # Try each cube
                    for cube_idx, cube in enumerate(cubes):
                        if used[cube_idx] or (cube.doppelganger and used[cube.doppelganger]):
                            continue  # Skip used cubes
                        # progress marker
                        solutions.rec_iter()
                        # Try all orientations of the current cube
                        for cube_with_orientation in cube.rotate():
                            if is_valid(sides, cube_with_orientation, x, y, z, size):
                                board[x][y][z] = cube_with_orientation
                                update_sides(sides, cube_with_orientation, x, y, z, size)
                                used[cube_idx] = True
                                if cube_with_orientation.doppelganger:
                                    used[cube_with_orientation.doppelganger] = True
                                if solve_sudoku_3d(board, sides, cubes, used, idx + 1, solutions):
                                    pass # look for more solutions

                                # Backtrack
                                board[x][y][z] = None
                                remove_cube_from_sides(sides, cube_with_orientation, x, y, z, size)
                                used[cube_idx] = False
                                if cube_with_orientation.doppelganger:
                                    used[cube_with_orientation.doppelganger] = False
                    return False
    return False


def print_board(board):
    for z in range(3):
        print(f"Layer {z}:")
        for y in range(3):
            # Create a list of string representations for each cube in the row
            row = [f"{board[x][y][z]}" for x in range(3)]
            print(' | '.join(row))
        print()


# Need to mark which ones are considered doubles so we don't over-use them
def expand_fuzzy69(cubeCollection: CubeCollection):
    fuzz = []
    idx = cubeCollection[-1].index + 1 # mark them as distinct
    for cube in cubeCollection:
        # Allow for possibility of a 6, a 9, or both on each cube
        if 6 in cube.faces:
            new_cube = Cube([9 if x == 6 else x for x in cube.faces], idx)
            idx += 1
            cube.doppelganger = new_cube.index
            new_cube.doppelganger = cube.index
            fuzz.append(new_cube)
        if 9 in cube.faces:
            new_cube = Cube([6 if x == 9 else x for x in cube.faces], idx)
            idx += 1
            cube.doppelganger = new_cube.index
            new_cube.doppelganger = cube.index
            fuzz.append(new_cube)
    print(f'Extending cube collection by {len(fuzz)} for 6 / 9 ambiguity, marking doppelgangers')
    cubeCollection.extend(fuzz)

# Create an empty nxnxn board, where each cell starts with a default cube (empty)
CUBE_LEN = 3
board = [[[None for _ in range(CUBE_LEN)] for _ in range(CUBE_LEN)] for _ in range(CUBE_LEN)]
# Efficiently keep track of which numbers are placed on each side. Order top, bottom, left, right, front, back
sides = [set() for _ in range(6)]

# Specific problem to solve
cubes = CubeCollection([
    # order top, bottom, left, right, front, back. 0=blank. 9s and 6s are equivalent.

    # blank
    [0, 0, 0, 0, 0, 0], #0

    # one marked
    [3, 0, 0, 0, 0, 0], #1
    [4, 0, 0, 0, 0, 0], #2
    [7, 0, 0, 0, 0, 0], #3
    [8, 0, 0, 0, 0, 0], #4
    [8, 0, 0, 0, 0, 0], #5
    [9, 0, 0, 0, 0, 0], #6

    # two marked
    [1, 0, 0, 0, 9, 0], #7
    [3, 0, 0, 0, 2, 0], #8
    [7, 0, 0, 5, 0, 0], #9
    [4, 0, 0, 5, 0, 0], #10=A
    [4, 0, 0, 0, 0, 8], #11=B
    [5, 0, 0, 9, 0, 0], #12=C
    [6, 0, 0, 5, 0, 0], #13=D
    [7, 0, 0, 0, 0, 6], #14=E
    [3, 0, 0, 0, 9, 0], #15=F
    [7, 0, 0, 4, 0, 0], #16=G
    [7, 0, 0, 0, 9, 0], #17=H
    [4, 0, 0, 0, 0, 6], #18=I

    # three marked
    [1, 0, 3, 0, 1, 0], #19=J
    [7, 0, 0, 3, 5, 0], #20=K
    [4, 0, 2, 0, 2, 0], #21=L
    [9, 0, 2, 0, 0, 1], #22=M
    [5, 0, 6, 0, 0, 8], #23=N
    [8, 0, 0, 1, 0, 8], #24=O
    [3, 0, 1, 0, 6, 0], #25=P
    [2, 0, 0, 6, 2, 0], #26=Q
])
assert len(cubes) == CUBE_LEN **3
# expand the list to allow for fuzzy matching of 6s and 9s, treat them as having MORE cubes to choose from
expand_fuzzy69(cubes)
print(cubes, '\n')
print('Possible permutations of all cube orientations, including ambiguous 6/9s:',cubes.permutations())

used = [False] * len(cubes)
iters=0
solutions = Solutions()
# Try solving the puzzle
solve_sudoku_3d(board, sides, cubes, used, 0, solutions)