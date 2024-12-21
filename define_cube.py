from marks import Marks, Sides
from ordered_set import OrderedSet

class Cube:
    def __init__(self, faces:list, id:int):
        assert len(faces) == 6
        assert id <= 26
        self.faces = faces  # A list with six numbers, 0 if face is blank
        self.id = id

    def __getitem__(self, side: Sides):
        return self.faces[side.value]

    # Count the number of nonblank faces
    def nonblanks(self):
        return sum(1 for x in self.faces if x > 0)

    def __str__(self):
        faces_str = ' '.join(str(face) if face >0 else '-' for face in self.faces)
        return f'{faces_str}'

    # Variants no longer need to be cached, as are used from slots
    def variants(self):
        v = rotations(self)
        alt = alternate_69(self)
        if alt.faces != self.faces:
            v.extend(rotations(alt))
        return v


# Return an alternative cube due to 6 / 9 ambiguity
def alternate_69(cube:Cube) -> Cube:
    swap = [0, 1, 2, 3, 4, 5, 9, 7, 8, 6]
    alt = list(map(lambda face: swap[face], cube.faces))
    return Cube(alt, cube.id)

# Return a list of up to 24 unique orientations of a cube
def rotations(cube:Cube) -> list:
    def oriented_as(c: Cube, mapping):
        """
        Reorient the cube according to a specific face mapping.

        Args:
            c (Cube): The cube to reorient.
            mapping (tuple[int]): Indices for the new orientation.

        Returns:
            tuple: The reoriented cube's faces in (top, bottom, left, right, front, back) order.
        """
        return tuple(c.faces[i] for i in mapping)

    # Define mappings, each is an orientation of the cube with a specific face at the top:
    # [top, bottom, left, right, front, back], in each of 4 rotations around the vertical axis
    face_mappings = [
        (0, 1, 2, 3, 4, 5), # Top is 0, rotation 0
        (0, 1, 4, 5, 3, 2), # Top is 0, rotation 1
        (0, 1, 3, 2, 5, 4), # Top is 0, rotation 2
        (0, 1, 5, 4, 2, 3), # Top is 0, rotation 3
        (1, 0, 3, 2, 4, 5), # Top is 1, rotation 0
        (1, 0, 4, 5, 2, 3), # Top is 1, rotation 1
        (1, 0, 2, 3, 5, 4), # Top is 1, rotation 2
        (1, 0, 5, 4, 3, 2), # Top is 1, rotation 3
        (2, 3, 0, 1, 5, 4), # Top is 2, rotation 0
        (2, 3, 5, 4, 1, 0), # Top is 2, rotation 1
        (2, 3, 1, 0, 4, 5), # Top is 2, rotation 2
        (2, 3, 4, 5, 0, 1), # Top is 2, rotation 3
        (3, 2, 1, 0, 5, 4), # Top is 3, rotation 0
        (3, 2, 5, 4, 0, 1), # Top is 3, rotation 1
        (3, 2, 0, 1, 4, 5), # Top is 3, rotation 2
        (3, 2, 4, 5, 1, 0), # Top is 3, rotation 3
        (4, 5, 2, 3, 1, 0), # Top is 4, rotation 0
        (4, 5, 1, 0, 3, 2), # Top is 4, rotation 1
        (4, 5, 3, 2, 0, 1), # Top is 4, rotation 2
        (4, 5, 0, 1, 2, 3), # Top is 4, rotation 3
        (5, 4, 3, 2, 1, 0), # Top is 5, rotation 0
        (5, 4, 1, 0, 2, 3), # Top is 5, rotation 1
        (5, 4, 2, 3, 0, 1), # Top is 5, rotation 2
        (5, 4, 0, 1, 3, 2), # Top is 5, rotation 3
    ]
    # Generate unique orientations as tuples
    unique_orientations = {
        oriented_as(cube, mapping) for mapping in face_mappings
    }

    # Return Cube objects for each unique orientation
    return [Cube(faces, cube.id) for faces in unique_orientations]

# There is always one cube completely blank. Each cube can have variants due to 6 / 9 and different rotations
class CubeCollection:
    def __init__(self, f_list:list):
        self.marked_cubes = [OrderedSet() for _ in range(len(Marks))]
        for id, faces in enumerate(f_list):
            c = Cube(faces, id)
            marks = c.nonblanks()
            self.marked_cubes[marks].add(c)
        return

    def __iter__(self):
        for cubes_set in self.marked_cubes:
            yield from cubes_set  # Yield each cube from the OrderedSet

# A canonical cube and its arbitrary list of variants
class CubeVariants:
    def __init__(self, cube: Cube, variants: list[Cube]):
        self.cube_id = cube.id
        self.variants = variants

    def __str__(self):
        variants_str = " , ".join(map(str, self.variants))
        return f"{self.cube.id}: [{variants_str}]"
