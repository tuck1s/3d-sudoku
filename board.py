
from marks import Sides
from define_cube import Cube

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
    def __init__(self, board:Board):
        self.board = board
        self.sides = [set() for _ in range(len(Sides))]
        self.piece = [None for _ in range(len(board.strip))]
        self.used = set()

    # place a cube
    def place_cube(self, visible: list, pos:int, cube:Cube, variant:Cube):
        self.used.add(cube) # use the canonical cube
        self.piece[pos] = variant
        # Add the marked faces to the corresponding board sides
        for i in visible:
            face = i.value
            self.sides[face].add(variant.faces[face])
        return

    # unplace a cube when backtracking
    def unplace_cube(self, visible:list, pos:int, cube:Cube, variant:Cube):
        self.used.remove(cube)  # remove the canonical cube
        self.piece[pos] = None
        # Remove the marked faces of the corresponding board sides
        for i in visible:
            face = i.value
            self.sides[face].remove(variant.faces[face])
        return

    # Is it valid to place a cube variant at this position into the board state?
    # If variant shows a blank face -> invalid
    # If variant shows a number that is already on the corresponding "big cube" side -> invalid
    def is_valid(self, visible:list, variant:Cube) -> bool:
        for i in visible:
            face = i.value
            if variant.faces[face] == 0 or variant.faces[face] in self.sides[face]:
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
