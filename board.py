
from marks import Sides
from define_cube import Cube, CubeCollection, CubeVariants

# A slot within the linear board (strip) representation
class BoardSlot:
    def __init__(self, sides_touched:set):
        self.sides_touched = sides_touched

class Board:
    def __init__(self, size):
        def get_sides(i: int, start: Sides, end: Sides) -> list:
            if i == 0:
                return [start]
            elif i == size - 1:
                return [end]
            return []

        # Provide lookup access to the pieces in the strip in terms of (x, y, z) location
        self.grid = [[[None for _ in range(size)] for _ in range(size)] for _ in range(size)]

        # Organize the board as an linear strip, knowing which "big cube" sides this piece touches
        self.strip = []

        # Iterate over all permutations of the positions, determining the affected sides
        for z in range(size):
            for y in range(size):
                for x in range(size):
                    sides_touched = set(
                        get_sides(x, Sides.left, Sides.right) +
                        get_sides(y, Sides.back, Sides.front) +
                        get_sides(z, Sides.bottom, Sides.top)
                    )
                    self.strip.append(BoardSlot(sides_touched))
                    self.grid[x][y][z] = len(self.strip)-1 # pos of strip element just added
        return


# The temporary board state as a solution is explored, each piece is indexed by strip position
class State:
    def __init__(self, board: Board, cubes: CubeCollection):
        self.board = board
        self.sides = [set() for _ in range(len(Sides))]  # Accumulate numbers on each "big cube" side
        self.piece = [None] * len(board.strip)
        self.used = set()
        self.visible = []
        self.cube_variants = []

        for slot in board.strip:
            visible = [side.value for side in slot.sides_touched]
            self.visible.append(visible)
            self.cube_variants.append(self._find_valid_variants(visible, cubes))
        return

    # Return the subset of cube variants that have numbers in the expected visible places
    def _find_valid_variants(self, visible, cubes):
        cube_candidates = cubes.marked_cubes[len(visible)]
        return [
            CubeVariants(c, [v for v in c.variants() if self.no_visible_blanks(visible, v)])
            for c in cube_candidates
        ]


    # place a cube
    def place_cube(self, visible: list[int], pos:int, cube:Cube, variant:Cube):
        self.used.add(cube) # use the canonical cube
        self.piece[pos] = variant
        # Add the marked faces to the corresponding board sides
        for face in visible:
            self.sides[face].add(variant.faces[face])
        return

    # unplace a cube when backtracking
    def unplace_cube(self, visible:list[int], pos:int, cube:Cube, variant:Cube):
        self.used.remove(cube)  # remove the canonical cube
        self.piece[pos] = None
        # Remove the marked faces of the corresponding board sides
        for face in visible:
            self.sides[face].remove(variant.faces[face])
        return

    # If variant shows a blank face -> invalid
    def no_visible_blanks(self, visible:list[int], variant:Cube) -> bool:
        for face in visible:
            if variant.faces[face] == 0:
                return False
        return True

    # Is it valid to place a cube variant at this position into the board state?
    # - simplified: we should never see a blank face
    # If variant shows a number that is already on the corresponding "big cube" side -> invalid
    def is_valid2(self, visible:list[int], variant:Cube) -> bool:
        for face in visible:
            if variant.faces[face] in self.sides[face]:
                return False
        return True

    def __str__(self):
        res = ''
        size = len(self.board.grid)
        for z in range(size):
            for y in range(size):
                for x in range(size):
                    pos = self.board.grid[x][y][z]
                    res += f'{self.piece[pos]} | '
                res += '\n'
            res += '\n'
        return res
