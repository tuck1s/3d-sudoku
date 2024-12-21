#!/usr/bin/env python3

# Import the Cube class and the cubes list from the cubes_definition file
from define_cube import CubeCollection
from board import Board, State
import time

def solve_sudoku_3d(board: Board, cubes: CubeCollection) -> int:

    # Search for cubes that fit a specific slot position
    def solve_from_pos(pos: int) -> bool:
        if pos >= depth:
            # print(state) # print the solution
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
                    if pos <= 8:
                        sols += solve_from_pos(pos+1)
                        elapsed_time = time.perf_counter() - start_time
                        print(f"{'-'*pos} with {variant}\t{elapsed_time:.3f}s\t {sols:,} solutions")
                    else:
                        sols += solve_from_pos_deep(pos+1) # no printing etc
                    state.unplace_cube(visible, pos, cube_id, variant) # Remove the face marks accruing from this
        return sols

    def solve_from_pos_deep(pos: int) -> bool:
        if pos >= depth:
            # print(state) # print the solution
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
    #FIXME: derive the first corner cube ID
    starting_corner = state.slot_cube_variants[0]
    v_list = list(starting_corner.ids)[0] # just pick the first variant, solution symmetries mean all variants are equivalent
    variant = starting_corner.variants[v_list][0]
    visible = state.visible[0]
    assert state.is_valid2(visible, variant)
    state.place_cube(visible, 0, variant.id, variant)
    sols = solve_from_pos(1)
    return sols

# Create an empty n x n x n board, where each cell starts with a default cube (empty)
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
# random.shuffle(pieces) # add randomness so we get to see different starting solutions
cubes = CubeCollection(pieces)
# Try solving the puzzle
sols = solve_sudoku_3d(board, cubes)
print(f'Solutions found: {sols:,}')
