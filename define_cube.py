from itertools import permutations

class Cube:
    def __init__(self, faces, index=None):
        self.faces = faces  # A list with six numbers, 0 if face is blank
        self.index = index  # Optional index for identification
        return

    # Return a set of up to 24 unique orientations of this cube, as a set of Cube
    # duplicates which may be caused by having the same numbers (or blanks) on some faces
    def rotate(self):
        def add_pos(top_idx, bottom_idx, left_idx, right_idx, front_idx, back_idx):
            new_faces = (
                self.faces[top_idx],     # Top
                self.faces[bottom_idx],  # Bottom
                self.faces[left_idx],    # Left
                self.faces[right_idx],   # Right
                self.faces[front_idx],   # Front
                self.faces[back_idx]     # Back
            )
            orientations.add(Cube(new_faces, index=self.index)) # create as tuple

        # All unique orientations of the cube (up to 24), skipping
        orientations = set()
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
        return orientations

    # Count the number of nonblank faces
    def nonblanks(self):
        return sum(1 for x in self.faces if x > 0)

    def __str__(self):
        faces_str = ' '.join(str(face) if face >0 else '-' for face in self.faces)
        return f"{self.index:2} Faces: {faces_str}"

class CubeCollection:
    def __init__(self, faces:list):
        self.cubes = []
        for i, v in enumerate(faces):
            self.cubes.append(Cube(v, index=i))

    def __len__(self):
        return len(self.cubes)

    def get(self, n:int) -> Cube:
        return self.cubes[n]