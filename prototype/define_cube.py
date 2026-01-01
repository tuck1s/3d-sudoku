from marks import Marks, Sides
from ordered_set import OrderedSet

class Cube:
    def __init__(self, faces:list, id:int):
        assert len(faces) == 6
        assert id <= 26
        self.faces = faces  # A list with six numbers, 0 if face is blank
        self.id = id

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
    def rotate_x(faces: tuple) -> tuple:
        """90° rotation around x-axis (left-right axis)"""
        return (faces[Sides.front.value], faces[Sides.back.value], faces[Sides.left.value], faces[Sides.right.value], faces[Sides.bottom.value], faces[Sides.top.value])

    def rotate_y(faces: tuple) -> tuple:
        """90° rotation around y-axis (front-back axis)"""
        return (faces[Sides.left.value], faces[Sides.right.value], faces[Sides.bottom.value], faces[Sides.top.value], faces[Sides.front.value], faces[Sides.back.value])

    def rotate_z(faces: tuple) -> tuple:
        """90° rotation around z-axis (top-bottom axis)"""
        return (faces[Sides.top.value], faces[Sides.bottom.value], faces[Sides.front.value], faces[Sides.back.value], faces[Sides.right.value], faces[Sides.left.value])

    # Generate all 24 rotations by trying all rotation combinations
    unique_orientations = set()

    state_x = tuple(cube.faces)
    for _ in range(4):
        state_y = state_x
        for _ in range(4):
            state_z = state_y
            for _ in range(4):
                unique_orientations.add(state_z)
                state_z = rotate_z(state_z)
            state_y = rotate_y(state_y)
        state_x = rotate_x(state_x)

    # Check we have the expected number of unique orientations for the various cube types
    num_nonblanks = cube.nonblanks()
    expected_counts = {0:1, 1:6, 2:24, 3:24}
    assert len(unique_orientations) == expected_counts[num_nonblanks], \
        f"Cube ID {cube.id} with {num_nonblanks} nonblank faces has {len(unique_orientations)} unique orientations, expected {expected_counts[num_nonblanks]}"
    # Return Cube objects for each unique orientation
    return [Cube(faces, cube.id) for faces in unique_orientations]

# There is always one cube completely blank. Each cube can have variants due to 6 / 9 and different rotations
class CubeCollection:
    def __init__(self, f_list:list):
        self.marked_cubes = [OrderedSet() for _ in range(len(Marks))]

        # Canonical positions for marked faces: top, left, front
        canonical_positions = [Sides.top.value, Sides.left.value, Sides.front.value]

        for id, face_values in enumerate(f_list):
            # Convert tuple to full 6-element array with canonical positioning
            faces = [0] * 6
            for i, val in enumerate(face_values):
                faces[canonical_positions[i]] = val

            c = Cube(faces, id)
            marks = c.nonblanks()
            self.marked_cubes[marks].add(c)
        return

    def __iter__(self):
        for cubes_set in self.marked_cubes:
            yield from cubes_set  # Yield each cube from the OrderedSet
