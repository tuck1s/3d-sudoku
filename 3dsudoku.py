# Import the Cube class and the cubes list from the cubes_definition file
from define_cube import Cube, CubeCollection

def is_interchangeable(a, b):
    # Treat 6 and 9 as interchangeable, and 0 as a wildcard (blank face)
    return (a == b) or (a == 6 and b == 9) or (a == 9 and b == 6) or a == 0 or b == 0

def is_valid(board, cube, x, y, z):
    print(f"Checking validity for cube at ({x}, {y}, {z}) with orientation {cube.faces}")

    if x > 0:  # Check left
        if not is_interchangeable(board[x-1][y][z].faces[3], cube.faces[2]):  # Left face
            print(f"Invalid: Left face mismatch at ({x-1}, {y}, {z})")
            return False
    if x < 2:  # Check right
        if not is_interchangeable(board[x+1][y][z].faces[2], cube.faces[3]):  # Right face
            print(f"Invalid: Right face mismatch at ({x+1}, {y}, {z})")
            return False
    if y > 0:  # Check front
        if not is_interchangeable(board[x][y-1][z].faces[4], cube.faces[5]):  # Front face
            print(f"Invalid: Front face mismatch at ({x}, {y-1}, {z})")
            return False
    if y < 2:  # Check back
        if not is_interchangeable(board[x][y+1][z].faces[5], cube.faces[4]):  # Back face
            print(f"Invalid: Back face mismatch at ({x}, {y+1}, {z})")
            return False
    if z > 0:  # Check bottom
        if not is_interchangeable(board[x][y][z-1].faces[1], cube.faces[1]):  # Bottom face
            print(f"Invalid: Bottom face mismatch at ({x}, {y}, {z-1})")
            return False
    if z < 2:  # Check top
        if not is_interchangeable(board[x][y][z+1].faces[0], cube.faces[0]):  # Top face
            print(f"Invalid: Top face mismatch at ({x}, {y}, {z+1})")
            return False
    return True


def solve_sudoku_3d(board, cubes:CubeCollection, used, idx):
    if idx == len(cubes):
        print("All cubes placed successfully.")
        return True  # All cubes placed

    for x in range(3):
        for y in range(3):
            for z in range(3):
                if board[x][y][z].faces == [0]*6:  # Check for empty cube
                    print(f"Empty spot found at ({x}, {y}, {z})")
                    combinations = cubes.get(idx).rotate()
                    # print(f'Cube with {cubes[idx].nonblanks()} marked faces has combinations={len(combinations)}')
                    for cube_with_orientation in combinations:
                        if is_valid(board, cube_with_orientation, x, y, z):
                            board[x][y][z] = cube_with_orientation
                            used[idx] = True
                            print(f"Placing cube {idx} at ({x}, {y}, {z}) with orientation {cube_with_orientation.faces}")
                            if solve_sudoku_3d(board, cubes, used, idx+1):
                                return True
                            board[x][y][z] = empty_cube  # Backtrack
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


# Create an empty 3x3x3 board, where each cell starts with a default cube (empty)
empty_cube = Cube([0]*6)  # Create an empty cube with all faces as zero
board = [[[empty_cube for _ in range(3)] for _ in range(3)] for _ in range(3)]
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
used = [False] * len(cubes)

# Try solving the puzzle
if solve_sudoku_3d(board, cubes, used, 0):
    print("Sudoku Solved!")
    print_board(board)

else:
    print("No solution exists.")
