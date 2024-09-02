from itertools import permutations

class Cube:
    def __init__(self, faces, index=None):
        self.faces = faces  # A list with six numbers, 0 if face is blank
        self.index = index  # Optional index for identification
        return

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
            orientations.add(new_faces) # create as tuple

        # All unique orientations of the cube (up to 24), skipping
        # duplicates which may be caused by having the same numbers (or blanks) on some faces
        orientations = set()

        # Define face mappings as an array
        # Each row represents the mapping for a specific top face:
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
            # Retrieve the mappings for the current top face
            top_idx, bottom_idx, left_idx, right_idx, front_idx, back_idx = face_mappings[top]
            for _ in range(4):
                add_pos(top_idx, bottom_idx, left_idx, right_idx, front_idx, back_idx)
                # Rotate around the vertical axis (top and bottom faces constant) to generate 4 orientations
                left_idx, front_idx, right_idx, back_idx = front_idx, right_idx, back_idx, left_idx

        return list(orientations)

    def __str__(self):
        index_str = f"Index: {self.index}, " if self.index is not None else ""
        faces_str = ', '.join(str(face) if face is not None else 'D/C' for face in self.faces)  # 'D/C' for 'don't care'
        return f"{index_str}Faces: {faces_str}"

# order top, bottom, left, right, front, back
cubes = [
    Cube([1, 0, 3, 0, 1, 0], index=0),  # A cube with some faces filled
    Cube([7, 0, 0, 5, 0, 0], index=1),
    Cube([4, 0, 0, 5, 0, 0], index=2),
    Cube([4, 0, 0, 0, 0, 0], index=3),
    Cube([0, 0, 0, 0, 0, 0], index=4),
    Cube([4, 0, 2, 0, 2, 0], index=5),
    Cube([3, 0, 0, 0, 0, 0], index=6),
    Cube([7, 0, 0, 0, 0, 0], index=7),
    Cube([4, 0, 0, 0, 0, 8], index=8),
    Cube([5, 0, 0, 9, 0, 0], index=9),
    Cube([7, 0, 0, 3, 5, 0], index=10),
    Cube([9, 0, 2, 0, 0, 1], index=11),
    Cube([3, 0, 0, 0, 2, 0], index=12),
    Cube([5, 0, 6, 0, 0, 8], index=13),
    Cube([8, 0, 0, 1, 0, 8], index=14),
    Cube([1, 0, 0, 0, 9, 0], index=15),
    Cube([6, 0, 0, 5, 0, 0], index=16),
    Cube([7, 0, 0, 0, 0, 6], index=17),
    Cube([3, 0, 0, 0, 9, 0], index=18),
    Cube([8, 0, 0, 0, 0, 0], index=19),
    Cube([9, 0, 0, 0, 0, 0], index=20),
    Cube([3, 0, 1, 0, 6, 0], index=21),
    Cube([7, 0, 0, 4, 0, 0], index=22),
    Cube([7, 0, 0, 0, 9, 0], index=23),
    Cube([4, 0, 0, 0, 0, 6], index=24),
    Cube([2, 0, 0, 6, 2, 0], index=25),
    Cube([8, 0, 0, 0, 0, 0], index=26),
]