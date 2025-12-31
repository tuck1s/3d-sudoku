
from marks import Sides
from define_cube import Cube, CubeCollection

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


# A canonical cube and its arbitrary list of variants. The possible ids are tracked in a set for ease of filtering
class SlotVariants:
    def __init__(self):
        self.variants = {}
        self.ids = set()

    def add(self, cube, v_list):
        assert not cube.id in self.ids
        self.variants[cube.id] = v_list
        self.ids.add(cube.id)

# The temporary board state as a solution is explored, each piece is indexed by strip position
class State:
    def __init__(self, board: Board, cubes: CubeCollection):
        self.board = board
        self.sides = [set() for _ in range(len(Sides))]  # Accumulate numbers on each "big cube" side
        self.piece = [None] * len(board.strip)
        # self.used = set()
        self.available = set()
        self.visible = [[side.value for side in slot.sides_touched] for slot in board.strip]
        self.slot_cube_variants = [SlotVariants() for _ in board.strip]

        # Add all cube variants into the slot states
        for marks, c_list in enumerate(cubes.marked_cubes):
            for c in c_list:
                self.available.add(c.id) # Add the canonical cube to the "available" list
                variants = c.variants()
                for i in range(len(self.visible)): # look at all slots
                    if len(self.visible[i]) == marks: # possible cube candidate
                        valid_variants = set()
                        for v in variants:
                            if self.no_visible_blanks(self.visible[i], v):
                                valid_variants.add(v)
                        # Got cube and variants to append
                        self.slot_cube_variants[i].add(c, list(valid_variants))
        return

    # place a cube
    def place_cube(self, visible: list[int], pos:int, cube_id:int, variant:Cube):
        self.available.remove(cube_id)
        self.piece[pos] = variant
        # Add the marked faces to the corresponding board sides
        for face in visible:
            self.sides[face].add(variant.faces[face])
        return

    # unplace a cube when backtracking
    def unplace_cube(self, visible:list[int], pos:int, cube_id:int, variant:Cube):
        self.available.add(cube_id)
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
