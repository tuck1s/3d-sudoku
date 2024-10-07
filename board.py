
from marks import Marks, Sides

class Board:
    def __init__(self, size):
        def get_sides(i: int, start: Sides, end: Sides) -> list:
            if i == 0:
                return [start]
            elif i == size - 1:
                return [end]
            return []

        # Co-ordinate access to the slots
        self.grid = [[[None for _ in range(size)] for _ in range(size)] for _ in range(size)]

        # Organize the board as an indexed list of centre, face, edge and corner slots for pieces
        self.slots = [ [] for _ in range(len(Marks))]

        # Iterate over all permutations of the positions, determining the affected sides
        for x in range(size):
            for y in range(size):
                for z in range(size):
                    sides_touched = (
                        get_sides(x, Sides.left, Sides.right) +
                        get_sides(y, Sides.back, Sides.front) +
                        get_sides(z, Sides.bottom, Sides.top)
                    )
                    print(f'Slot ({x}, {y}, {z}) touches sides {sides_touched}')
                    marks = len(sides_touched) # This slot requires pieces with this number of faces marked
                    self.slots[marks].append( {
                        'sides': sides_touched,
                        'pos': (x, y, z),
                        'piece': None,
                    })
                    self.grid[x][y][z] = self.slots[marks]
        # Efficiently keep track of which numbers are already placed on each side
        self.sides = [set() for _ in range(len(Sides))]
        return


