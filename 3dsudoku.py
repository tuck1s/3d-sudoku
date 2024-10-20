#!/usr/bin/env python3

# Import the Cube class and the cubes list from the cubes_definition file
from define_cube import Cube, CubeCollection
from board import Board, BoardSlot
from solutions import Solutions
from marks import Sides
from copy import deepcopy
'''
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
'''

# The temporary board state as a solution is explored
class State:
    def __init__(self, n:int):
        self.sides = [set() for _ in range(len(Sides))]
        self.piece = [None for _ in range(n)]

    # place a cube in a board slot
    def place_cube(self, idx:int, cube):
        self.piece[idx] = cube
        # Add the marked faces to the corresponding board sides
        for i in range(len(cube.faces)):
            self.sides[i].add(cube.faces[i])
        return

    def unplace_cube(self, idx:int, cube):
        self.piece[idx] = None
        # Add the marked faces to the corresponding board sides
        for i in range(len(cube.faces)):
            self.sides[i].remove(cube.faces[i])

    def __str__(self):
        res = ''
        for p in self.piece:
            res += str(p) + ' '
        return res

# Is it valid to place a cube variant at this position on the board?
# If any number on this cube variant already appears on the corresponding side, then it's not valid
def is_valid(state: State, board:Board, pos:int, cube:Cube) -> bool:
    # Check this cube has numbers showing on its faces that will be visible
    for face in board.strip[pos].sides_touched:
        if cube.faces[face.value] == 0:
            return False
    for i in range(len(cube.faces)):
        if cube.faces[i] in state.sides[i]:
            return False
    return True


def solve_sudoku_3d(board: Board, cubes: CubeCollection, solutions:Solutions) -> bool:

    # Iterate over a specific slot position
    def solve_from_pos(pos: int) -> bool:
        if pos >= len(board.strip):
            print('Got to end of strip')
            return True

        marks = len(board.strip[pos].sides_touched) # look for candidate pieces that have the expected number of face marks
        # Try all cubes with the required number of face marks
        for cube in cubes.marked_cubes[marks]:
            # Try all variants of this cube
            variants = cube.variants()
            for variant in variants:
                print(f'{"-"*pos}trying {cube} variant {variant}')
                if is_valid(state, board, pos, variant):
                    state.place_cube(pos, variant)
                    print(state)
                    # TODO: remove used cubes from possibles as we go, will need another struct
                    solved = solve_from_pos(pos+1)
                    if solved:
                        return True
                    else:
                        state.unplace_cube(pos, variant) # Remove the face marks accruing from this
        # Tried all cubes, nothing fits
        return False

    state = State(len(board.strip))
    solved = solve_from_pos(0)
    print(solved)



    '''
    # Iterate over all permutations of the positions
    for x in range(size):
        for y in range(size):
            for z in range(size):
                if board[x][y][z] is None:  # Check for empty spot
                    # Try each cube
                    for cube_idx, cube in enumerate(cubes):
                        if used[cube_idx] or (cube.doppelganger and used[cube.doppelganger]):
                            continue  # Skip used cubes
                        solutions.rec_iter() # progress marker
                        # Try all orientations of the current cube
                        for cube_with_orientation in cube.rotate():
                            if is_valid(sides, cube_with_orientation, x, y, z, size):
                                board[x][y][z] = cube_with_orientation
                                update_sides(sides, cube_with_orientation, x, y, z, size)
                                used[cube_idx] = True
                                if cube_with_orientation.doppelganger:
                                    used[cube_with_orientation.doppelganger] = True
                                if solve_sudoku_3d(board, sides, cubes, used, idx + 1, solutions):
                                    return True # pass # look for more solutions

                                # Backtrack
                                board[x][y][z] = None
                                remove_cube_from_sides(sides, cube_with_orientation, x, y, z, size)
                                used[cube_idx] = False
                                if cube_with_orientation.doppelganger:
                                    used[cube_with_orientation.doppelganger] = False
                    return False
    return False
    '''




# Create an empty nxnxn board, where each cell starts with a default cube (empty)
CUBE_LEN = 3
board = Board(CUBE_LEN)

# Specific problem to solve
pieces = [
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
]
assert len(pieces) == CUBE_LEN **3
cubes = CubeCollection(pieces)
for group in cubes.marked_cubes:
    for c in group:
        v = len(c.variants())
        print(f'Cube: {c}, variants: {v}')

iters=0
solutions = Solutions()
# Try solving the puzzle

#board.add(0, cubes.marked_cubes[0][0])
#print(board)
solve_sudoku_3d(board, cubes, solutions)