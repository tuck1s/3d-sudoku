#!/usr/bin/env python3

# Import the Cube class and the cubes list from the cubes_definition file
from define_cube import Cube, CubeCollection, rotations
from board import Board, State
import time

# Note hacked version that shows expected work for each of the slot[1] edge pieces

def solve_sudoku_3d(board: Board, cubes: CubeCollection) -> int:

    # Search for cubes that fit a specific slot position
    def solve_from_pos(pos: int) -> bool:
        # look for candidate pieces that have the expected number of visible faces, that are not already used.
        # For each cube position in the strip, the visible faces are already known
        #   - The possible cube variants that could fit are known (excluding any visible blank faces)

        visible = state.visible[pos]
        variants_pos = state.slot_cube_variants[pos]
        sols = 0 # number of solutions seen at this depth
        avail_ids = variants_pos.ids & state.available # Use set intersection to give a shortlist
        for cube_id in avail_ids: # The canonical cube being considered
            for variant in variants_pos.variants[cube_id]:  # The short list of variant orientations of this cube that might fit
                if state.is_valid2(visible, variant):
                    state.place_cube(visible, pos, cube_id, variant)
                    if pos <= 8:
                        sols += solve_from_pos(pos+1)
                        elapsed_time = time.perf_counter() - start_time
                        # print(f"{'-'*pos} with {variant}\t{elapsed_time:.3f}s\t {sols:,} solutions")
                    else:
                        sols += solve_from_pos_deep(pos+1) # no printing etc
                    state.unplace_cube(visible, pos, cube_id, variant) # Remove the face marks accruing from this
        return sols

    def solve_from_pos_deep(pos: int) -> bool:
        if pos >= depth:
            print(state) # print the solution
            return 1
        # look for candidate pieces that have the expected number of visible faces, that are not already used.
        # For each cube position in the strip, the visible faces are already known
        #   - The possible cube variants that could fit are known (excluding any visible blank faces)
        visible = state.visible[pos]
        variants_pos = state.slot_cube_variants[pos]
        sols = 0 # number of solutions seen at this depth
        avail_ids = variants_pos.ids & state.available # Use set intersection to give a shortlist
        for cube_id in avail_ids: # The canonical cube being considered
            for variant in variants_pos.variants[cube_id]:  # The short list of variant orientations of this cube that might fit
                if state.is_valid2(visible, variant):
                    state.place_cube(visible, pos, cube_id, variant)
                    sols += solve_from_pos_deep(pos+1) # no printing etc
                    state.unplace_cube(visible, pos, cube_id, variant) # Remove the face marks accruing from this
        return sols

    start_time = time.perf_counter()

    depth = len(board.strip)
    state = State(board, cubes)
    # Slot 0: force the first corner to always be the first piece (as solution symmetries mean there are 8x3x equivalent solutions)
    starting_corner = state.slot_cube_variants[0]
    cube_id = list(starting_corner.ids)[0] # just pick the first, solution symmetries mean all variants are equivalent
    variant = starting_corner.variants[cube_id][0]
    visible = state.visible[0]
    assert state.is_valid2(visible, variant)
    state.place_cube(visible, 0, cube_id, variant)
    sols = solve_from_pos(1)
    return sols

# Create an empty n x n x n board, where each cell starts with a default cube (empty)
CUBE_LEN = 3
board = Board(CUBE_LEN)

# Specific problem to solve. 9s and 6s are equivalent.
pieces = [
    # blank
    [], #0

    # one marked
    [3], #1
    [4], #2
    [7], #3
    [8], #4
    [8], #5
    [6], #6

    # two marked - in order top, left
    [1, 9], #7
    [3, 2], #8
    [7, 5], #9
    [4, 5], #10=A
    [4, 8], #11=B
    [5, 9], #12=C
    [6, 5], #13=D
    [7, 6], #14=E
    [3, 9], #15=F
    [7, 4], #16=G
    [7, 9], #17=H
    [4, 6], #18=I

    # three marked - in order top, left, front
    [1, 3, 1], #19=J
    [7, 5, 3], #20=K
    [4, 2, 2], #21=L
    [9, 1, 2], #22=M
    [5, 8, 6], #23=N
    [8, 1, 8], #24=O
    [3, 1, 6], #25=P
    [2, 2, 6], #26=Q
]
assert len(pieces) == CUBE_LEN **3
# random.shuffle(pieces) # add randomness so we get to see different starting solutions
cubes = CubeCollection(pieces)
# Try solving the puzzle
sols = solve_sudoku_3d(board, cubes)

print(f'Solutions found: {sols:,}')
