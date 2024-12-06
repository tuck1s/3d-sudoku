from marks import Marks, Sides

class Cube:
    def __init__(self, faces):
        assert len(faces) == 6
        self.faces = faces  # A list with six numbers, 0 if face is blank
        self.variants_cache = [] # Expand on-demand

    def __getitem__(self, side: Sides):
        return self.faces[side.value]

    # Count the number of nonblank faces
    def nonblanks(self):
        return sum(1 for x in self.faces if x > 0)

    def __str__(self):
        faces_str = ' '.join(str(face) if face >0 else '-' for face in self.faces)
        return f'{faces_str}'

    # Variants are created once, cached and returned
    def variants(self):
        if self.variants_cache:
            return self.variants_cache
        else:
            self.variants_cache = rotations(self)
            alt = alternate_69(self)
            if alt.faces != self.faces:
                self.variants_cache.extend(rotations(alt))
            return self.variants_cache


# Return an alternative cube due to 6 / 9 ambiguity
def alternate_69(cube:Cube) -> Cube:
    swap = [0, 1, 2, 3, 4, 5, 9, 7, 8, 6]
    alt = list(map(lambda face: swap[face], cube.faces))
    return Cube(alt)

# Return a list of up to 24 unique orientations of a cube
def rotations(cube:Cube) -> list:
    def add_pos(top_idx, bottom_idx, left_idx, right_idx, front_idx, back_idx):
        new_faces = (
            cube.faces[top_idx],     # Top
            cube.faces[bottom_idx],  # Bottom
            cube.faces[left_idx],    # Left
            cube.faces[right_idx],   # Right
            cube.faces[front_idx],   # Front
            cube.faces[back_idx]     # Back
        )
        face_tuple_set.add(new_faces) # create as tuple, so that duplicates are eliminated

    # All unique orientations of the cube (up to 24)
    face_tuple_set = set()
    # Define mappings, each is an orientation of the cube with a specific face at the top:
    # [top, bottom, left, right, front, back]
    face_mappings = [
        [0, 1, 2, 3, 4, 5],  # Top is 0
        [1, 0, 3, 2, 4, 5],  # Top is 1
        [2, 3, 0, 1, 5, 4],  # Top is 2
        [3, 2, 1, 0, 5, 4],  # Top is 3
        [4, 5, 2, 3, 1, 0],  # Top is 4
        [5, 4, 3, 2, 1, 0]   # Top is 5
    ]
    for top in range(len(face_mappings)):
        # Expand the mappings
        top_idx, bottom_idx, left_idx, right_idx, front_idx, back_idx = face_mappings[top]
        for _ in range(4):
            add_pos(top_idx, bottom_idx, left_idx, right_idx, front_idx, back_idx)
            # Rotate around the vertical axis (top and bottom faces kept constant) to generate 4 orientations
            left_idx, front_idx, right_idx, back_idx = front_idx, right_idx, back_idx, left_idx
    return [Cube(c) for c in face_tuple_set]


# There is always one cube completely blank. Each cube can have variants due to 6 / 9 and different rotations
class CubeCollection:
    def __init__(self, faces:list):
        self.marked_cubes = [ set() for _ in range(len(Marks))]
        for v in faces:
            c = Cube(v)
            marks = c.nonblanks()
            self.marked_cubes[marks].add(c)
        return

# A canonical cube and its arbitrary list of variants
class CubeVariants:
    def __init__(self, cube: Cube, variants: list[Cube]):
        self.cube = cube
        self.variants = variants

    def __str__(self):
        variants_str = ", ".join(map(str, self.variants))
        return f"{self.cube}: {variants_str}"
