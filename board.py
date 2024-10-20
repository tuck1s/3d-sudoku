
from marks import Marks, Sides

# A slot within the linear board (strip) representation
class BoardSlot:
    def __init__(self, sides_touched:set, pos:tuple):
        self.sides_touched = sides_touched
        self.pos = pos

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

        # Organize the board as an linear strip
        self.strip = []

        # Iterate over all permutations of the positions, determining the affected sides
        for x in range(size):
            for y in range(size):
                for z in range(size):
                    sides_touched = set(
                        get_sides(x, Sides.left, Sides.right) +
                        get_sides(y, Sides.back, Sides.front) +
                        get_sides(z, Sides.bottom, Sides.top)
                    )
                    # print(f'Slot ({x}, {y}, {z}) touches sides {sides_touched}')
                    self.strip.append(BoardSlot(sides_touched, (x, y, z)))
                    self.grid[x][y][z] = self.strip[-1] # strip element just added
        # Efficiently keep track of which numbers are already placed on each side
        return

    # pretty-print string representation of the board state
    def __str__(self):
        res = ''
        for z in range(len(self.grid)):
            res += f"Layer {z}:\n"
            for y in range(len(self.grid[0])):
                # Create a list of string representations for each cube in the row
                row = [f"{self.grid[x][y][z].piece}" for x in range(len(self.grid[0][0]))]
                res += ' | '.join(row) + '\n'
        return res