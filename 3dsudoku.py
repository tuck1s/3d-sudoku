# Import the Cube class and the cubes list from the cubes_definition file
from define_cube import Cube, CubeCollection, Sides
from typing import List, Set

def is_interchangeable(a, b):
    # Treat 6 and 9 as interchangeable, and 0 as a wildcard (blank face)
    return (a == b) or (a == 6 and b == 9) or (a == 9 and b == 6) or a == 0 or b == 0

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
            if cube[side] == 0:  # No blank face allowed
                # print(f"Not placing a blank {cube[side]} on the {side.name} face")
                return False
            if cube[side] in sides[side.value]:  # No repeating number on the same face
                print(f"Already got a {cube[side]} on the {side.name} face")
                return False
    return True

def update_sides(sides: List[Set[int]], cube: Cube, x: int, y: int, z: int, size: int):
    checks = generate_checks(x, y, z, size)
    for side in Sides:
        if checks[side]:
            sides[side.value].add(cube[side])
            # print(f"Added {cube[side]} to {side.name} set")

def remove_cube_from_sides(sides: List[Set[int]], cube: Cube, x: int, y: int, z: int, size: int):
    checks = generate_checks(x, y, z, size)

    for side in Sides:
        if checks[side]:
            sides[side.value].discard(cube[side])  # Use discard to avoid KeyError if the element is not present
            # print(f"Removed {cube[side]} from {side.name} set")

def solve_sudoku_3d(board:list, sides:List[Set[int]], cubes:CubeCollection, used, idx):
    if idx == len(cubes):
        print("All cubes placed successfully.")
        return True  # All cubes placed
    size = len(board)
    for x in range(size):
        for y in range(size):
            for z in range(size):
                if board[x][y][z] is None:  # Check for empty cube
                    print(f"Empty spot found at ({x}, {y}, {z})")
                    combinations = cubes.get(idx).rotate()
                    # print(f'Cube with {cubes[idx].nonblanks()} marked faces has combinations={len(combinations)}')
                    for cube_with_orientation in combinations:
                        if is_valid(sides, cube_with_orientation, x, y, z, size):
                            board[x][y][z] = cube_with_orientation
                            update_sides(sides, cube_with_orientation, x, y, z, size)
                            used[idx] = True
                            print(f"Placing cube {idx} at ({x}, {y}, {z}) with orientation {cube_with_orientation.faces}")
                            if solve_sudoku_3d(board, sides, cubes, used, idx+1):
                                return True
                            board[x][y][z] = None  # Backtrack
                            remove_cube_from_sides(sides, cube_with_orientation, x, y, z, size)
                            used[idx] = False
                            print(f"Backtracking from ({x}, {y}, {z})")
                    print(f"No valid placement for cube {idx} at ({x}, {y}, {z}) with all orientations, backtracking...")
                    return False
    print(f"No solution found with current configuration, idx: {idx}")
    return False


def print_board(board):
    for z in range(3):
        print(f"Layer {z}:")
        for y in range(3):
            # Create a list of string representations for each cube in the row
            row = [f"{board[x][y][z]}" for x in range(3)]
            print(' | '.join(row))
        print()


# Create an empty nxnxn board, where each cell starts with a default cube (empty)
CUBE_LEN = 3
board = [[[None for _ in range(CUBE_LEN)] for _ in range(CUBE_LEN)] for _ in range(CUBE_LEN)]
# Efficiently keep track of which numbers are placed on each side. Order top, bottom, left, right, front, back
sides = [set() for _ in range(6)]

cubes = CubeCollection([
    # order top, bottom, left, right, front, back. 0=blank. 9s and 6s are equivalent.
    [1, 0, 3, 0, 1, 0],  # Specific problem to solve
    [7, 0, 0, 5, 0, 0],
    [4, 0, 0, 5, 0, 0],
    [4, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0],
    [4, 0, 2, 0, 2, 0],
    [3, 0, 0, 0, 0, 0],
    [7, 0, 0, 0, 0, 0],
    [4, 0, 0, 0, 0, 8],
    [5, 0, 0, 9, 0, 0],
    [7, 0, 0, 3, 5, 0],
    [9, 0, 2, 0, 0, 1],
    [3, 0, 0, 0, 2, 0],
    [5, 0, 6, 0, 0, 8],
    [8, 0, 0, 1, 0, 8],
    [1, 0, 0, 0, 9, 0],
    [6, 0, 0, 5, 0, 0],
    [7, 0, 0, 0, 0, 6],
    [3, 0, 0, 0, 9, 0],
    [8, 0, 0, 0, 0, 0],
    [9, 0, 0, 0, 0, 0],
    [3, 0, 1, 0, 6, 0],
    [7, 0, 0, 4, 0, 0],
    [7, 0, 0, 0, 9, 0],
    [4, 0, 0, 0, 0, 6],
    [2, 0, 0, 6, 2, 0],
    [8, 0, 0, 0, 0, 0],
])
assert len(cubes) == CUBE_LEN **3
used = [False] * len(cubes)

# Try solving the puzzle
if solve_sudoku_3d(board, sides, cubes, used, 0):
    print("Sudoku Solved!")
    print_board(board)

else:
    print("No solution exists.")
