from enum import Enum

# Convention used for numbering the sides of the cube (and the board)
class Sides(Enum):
    top = 0
    bottom = 1
    left = 2
    right = 3
    front = 4
    back = 5

# Depending on number of nonblank faces, which can be 0, 1, 2 or 3 numeric markings
#   0 marks -> centre of cube
#   1 mark  -> face pieces - 6 of them
#   2 marks -> edge (vertex) pieces - 12 of them
#   3 marks -> corner pieces - 8 of them
class Marks(Enum):
    centre = 0
    face = 1
    edge = 2
    corner = 3

