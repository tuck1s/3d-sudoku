#!/usr/bin/env python3

# Import the Cube class and the cubes list from the cubes_definition file
from define_cube import CubeCollection
from board import Board, State
from solutions import Solutions
import random

def solve_sudoku_3d(board: Board, cubes: CubeCollection, solutions:Solutions) -> bool:

    # Search for cubes that fit a specific slot position
    def solve_from_pos(pos: int) -> bool:
        if pos >= len(board.strip):
            solutions.add(state)
            return False # set to False to keep looking for other solutions

        # look for candidate pieces that have the expected number of visible faces, that are not already used. Reduce to list of int index values
        visible = [i.value for i in board.strip[pos].sides_touched]
        for cube in cubes.marked_cubes[len(visible)]:
            if not cube in state.used:
                for variant in cube.variants():
                    if state.is_valid(visible, variant):
                        state.place_cube(visible, pos, cube, variant)
                        if solve_from_pos(pos+1):
                            return True
                        else:
                            state.unplace_cube(visible, pos, cube, variant) # Remove the face marks accruing from this
        return False # Tried all cubes, nothing fits

    state = State(board)
    return solve_from_pos(0)

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
random.shuffle(pieces) # add randomness so we get to see different starting solutions
cubes = CubeCollection(pieces)
solutions = Solutions(board)
# Try solving the puzzle
solve_sudoku_3d(board, cubes, solutions)
print(f'Solutions found: {solutions.total}')
