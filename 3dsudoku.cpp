#include <iostream>
#include <vector>
#include <array>
#include <set>
#include <cassert>
#include <chrono>
#include <iomanip>
#include <cstring>
#include <locale>

const int DEPTH_TO_PRINT = 8;

// Sides enum
enum Sides {
    TOP = 0,
    BOTTOM = 1,
    LEFT = 2,
    RIGHT = 3,
    FRONT = 4,
    BACK = 5
};

// Marks enum
enum Marks {
    CENTRE = 0,
    FACE = 1,
    EDGE = 2,
    CORNER = 3
};

// Bitmask utility functions
inline bool bitmask_contains(uint64_t mask, int val) {
    return (mask & (1ull << val)) != 0;
}

inline void bitmask_add(uint64_t& mask, int val) {
    mask |= (1ull << val);
}

inline void bitmask_remove(uint64_t& mask, int val) {
    mask &= ~(1ull << val);
}

inline uint64_t bitmask_intersection(uint64_t a, uint64_t b) {
    return a & b;
}

inline int bitmask_popcount(uint64_t mask) {
    return __builtin_popcountll(mask);
}

// Get first set bit position (0-indexed), returns -1 if empty
inline int bitmask_first(uint64_t mask) {
    if (mask == 0) return -1;
    return __builtin_ctzll(mask);
}

// Cube class
class Cube {
public:
    std::array<int, 6> faces;
    int id;

    Cube() : id(-1) {
        faces.fill(0);
    }

    Cube(const std::array<int, 6>& f, int cube_id) : faces(f), id(cube_id) {}

    int nonblanks() const {
        int count = 0;
        for (int face : faces) {
            if (face > 0) count++;
        }
        return count;
    }

    bool operator==(const Cube& other) const {
        return faces == other.faces;
    }

    bool operator!=(const Cube& other) const {
        return !(*this == other);
    }

    std::string to_string() const {
        std::string result;
        for (int face : faces) {
            if (face > 0) {
                result += std::to_string(face) + " ";
            } else {
                result += "- ";
            }
        }
        if (!result.empty()) result.pop_back(); // Remove trailing space
        return result;
    }
};

// Return an alternative cube due to 6/9 ambiguity
Cube alternate_69(const Cube& cube) {
    static const int swap[] = {0, 1, 2, 3, 4, 5, 9, 7, 8, 6};
    std::array<int, 6> alt;
    for (int i = 0; i < 6; i++) {
        alt[i] = swap[cube.faces[i]];
    }
    return Cube(alt, cube.id);
}

// Return a list of up to 24 unique orientations of a cube
std::vector<Cube> rotations(const Cube& cube) {
    auto rotate_x = [](const std::array<int, 6>& faces) -> std::array<int, 6> {
        // 90° rotation around x-axis (left-right axis)
        return {faces[FRONT], faces[BACK], faces[LEFT], faces[RIGHT], faces[BOTTOM], faces[TOP]};
    };

    auto rotate_y = [](const std::array<int, 6>& faces) -> std::array<int, 6> {
        // 90° rotation around y-axis (front-back axis)
        return {faces[LEFT], faces[RIGHT], faces[BOTTOM], faces[TOP], faces[FRONT], faces[BACK]};
    };

    auto rotate_z = [](const std::array<int, 6>& faces) -> std::array<int, 6> {
        // 90° rotation around z-axis (top-bottom axis)
        return {faces[TOP], faces[BOTTOM], faces[FRONT], faces[BACK], faces[RIGHT], faces[LEFT]};
    };

    // Generate all 24 rotations by trying all rotation combinations
    std::vector<std::array<int, 6>> unique_orientations;

    std::array<int, 6> state_x = cube.faces;
    for (int x = 0; x < 4; x++) {
        std::array<int, 6> state_y = state_x;
        for (int y = 0; y < 4; y++) {
            std::array<int, 6> state_z = state_y;
            for (int z = 0; z < 4; z++) {
                // Check if this orientation is unique
                bool found = false;
                for (const auto& existing : unique_orientations) {
                    if (existing == state_z) {
                        found = true;
                        break;
                    }
                }
                if (!found) {
                    unique_orientations.push_back(state_z);
                }
                state_z = rotate_z(state_z);
            }
            state_y = rotate_y(state_y);
        }
        state_x = rotate_x(state_x);
    }

    // Check we have the expected number of unique orientations for the various cube types
    int num_nonblanks = cube.nonblanks();
    int expected_counts[] = {1, 6, 24, 24};
    int expected = expected_counts[num_nonblanks];
    if (unique_orientations.size() != expected) {
        std::cerr << "Cube ID " << cube.id << " with " << num_nonblanks
                  << " nonblank faces has " << unique_orientations.size()
                  << " unique orientations, expected " << expected << std::endl;
        assert(false);
    }

    std::vector<Cube> result;
    for (const auto& faces : unique_orientations) {
        result.emplace_back(faces, cube.id);
    }
    return result;
}

// Get all variants of a cube (rotations + 6/9 alternates)
std::vector<Cube> get_variants(const Cube& cube) {
    std::vector<Cube> v = rotations(cube);
    Cube alt = alternate_69(cube);
    if (alt != cube) {
        std::vector<Cube> alt_rots = rotations(alt);
        v.insert(v.end(), alt_rots.begin(), alt_rots.end());
    }
    return v;
}

// CubeCollection class
class CubeCollection {
public:
    std::array<std::vector<Cube>, 4> marked_cubes; // 4 = number of Marks values

    CubeCollection(const std::vector<std::vector<int>>& f_list) {
        // Canonical positions: TOP, LEFT, FRONT
        const int canonical_positions[] = {TOP, LEFT, FRONT};

        for (int id = 0; id < f_list.size(); id++) {
            const std::vector<int>& face_values = f_list[id];

            // Expand to full 6-element array with canonical positioning
            std::array<int, 6> faces = {0, 0, 0, 0, 0, 0};
            for (int i = 0; i < face_values.size(); i++) {
                faces[canonical_positions[i]] = face_values[i];
            }

            Cube c(faces, id);
            int marks = c.nonblanks();
            marked_cubes[marks].push_back(c);
        }
    }
};

// BoardSlot class
class BoardSlot {
public:
    uint64_t sides_touched; // bitmask of Sides

    BoardSlot(uint64_t sides) : sides_touched(sides) {}
};

// Board class
class Board {
public:
    std::vector<std::vector<std::vector<int>>> grid;
    std::vector<BoardSlot> strip;
    int size;

    Board(int sz) : size(sz) {
        grid.resize(sz, std::vector<std::vector<int>>(sz, std::vector<int>(sz, -1)));

        auto get_sides = [sz](int i, Sides start, Sides end) -> uint64_t {
            uint64_t mask = 0;
            if (i == 0) {
                bitmask_add(mask, start);
            } else if (i == sz - 1) {
                bitmask_add(mask, end);
            }
            return mask;
        };

        for (int z = 0; z < sz; z++) {
            for (int y = 0; y < sz; y++) {
                for (int x = 0; x < sz; x++) {
                    uint64_t sides_touched =
                        get_sides(x, LEFT, RIGHT) |
                        get_sides(y, BACK, FRONT) |
                        get_sides(z, BOTTOM, TOP);

                    strip.emplace_back(sides_touched);
                    grid[x][y][z] = strip.size() - 1;
                }
            }
        }
    }
};

// SlotVariants class
class SlotVariants {
public:
    std::vector<std::vector<Cube>> variants; // variants[cube_id] = list of variants
    uint64_t ids; // bitmask of cube IDs

    SlotVariants() : ids(0) {
        variants.resize(27);
    }

    void add(const Cube& cube, const std::vector<Cube>& v_list) {
        assert(!bitmask_contains(ids, cube.id));
        variants[cube.id] = v_list;
        bitmask_add(ids, cube.id);
    }
};

// State class
class State {
public:
    Board* board;
    std::array<uint64_t, 6> sides; // bitmask of numbers (1-9) on each side
    std::vector<Cube> piece;
    uint64_t available; // bitmask of available cube IDs
    std::vector<std::vector<int>> visible; // visible[pos] = list of visible face indices
    std::vector<SlotVariants> slot_cube_variants;

    State(Board* b, CubeCollection* cubes) : board(b) {
        sides.fill(0);
        piece.resize(board->strip.size());
        available = 0;
        visible.resize(board->strip.size());
        slot_cube_variants.resize(board->strip.size());

        // Populate visible faces for each slot
        for (int i = 0; i < board->strip.size(); i++) {
            uint64_t sides_mask = board->strip[i].sides_touched;
            for (int side = 0; side < 6; side++) {
                if (bitmask_contains(sides_mask, side)) {
                    visible[i].push_back(side);
                }
            }
        }

        // Add all cube variants into slot states
        for (int marks = 0; marks < 4; marks++) {
            for (const Cube& c : cubes->marked_cubes[marks]) {
                bitmask_add(available, c.id);
                std::vector<Cube> variants = get_variants(c);

                for (int i = 0; i < visible.size(); i++) {
                    if (visible[i].size() == marks) {
                        std::vector<Cube> valid_variants;
                        for (const Cube& v : variants) {
                            if (no_visible_blanks(visible[i], v)) {
                                valid_variants.push_back(v);
                            }
                        }
                        if (!valid_variants.empty()) {
                            slot_cube_variants[i].add(c, valid_variants);
                        }
                    }
                }
            }
        }
    }

    inline void place_cube(const std::vector<int>& vis, int pos, int cube_id, const Cube& variant) {
        bitmask_remove(available, cube_id);
        piece[pos] = variant;
        const int* faces = variant.faces.data();
        for (int face : vis) {
            bitmask_add(sides[face], faces[face]);
        }
    }

    inline void unplace_cube(const std::vector<int>& vis, int pos, int cube_id, const Cube& variant) {
        bitmask_add(available, cube_id);
        piece[pos] = Cube();
        const int* faces = variant.faces.data();
        for (int face : vis) {
            bitmask_remove(sides[face], faces[face]);
        }
    }

    bool no_visible_blanks(const std::vector<int>& vis, const Cube& variant) const {
        for (int face : vis) {
            if (variant.faces[face] == 0) {
                return false;
            }
        }
        return true;
    }

    inline bool is_valid2(const std::vector<int>& vis, const Cube& variant) const {
        const int* faces = variant.faces.data();
        for (int face : vis) {
            if (bitmask_contains(sides[face], faces[face])) {
                return false;
            }
        }
        return true;
    }

    std::string to_string() const {
        std::string res;
        for (int z = 0; z < board->size; z++) {
            for (int y = 0; y < board->size; y++) {
                for (int x = 0; x < board->size; x++) {
                    int pos = board->grid[x][y][z];
                    res += piece[pos].to_string() + " | ";
                }
                res += "\n";
            }
            res += "\n";
        }
        return res;
    }
};

// Global variables for solver
State* g_state = nullptr;
int g_depth = 0;
auto g_start_time = std::chrono::high_resolution_clock::now();

// Forward declarations
uint64_t solve_from_pos(int pos);
uint64_t solve_from_pos_deep(int pos);

uint64_t solve_from_pos(int pos) {
    const std::vector<int>& visible = g_state->visible[pos];
    SlotVariants& variants_pos = g_state->slot_cube_variants[pos];
    uint64_t sols = 0;

    const uint64_t avail_ids = bitmask_intersection(variants_pos.ids, g_state->available);

    // Iterate through set bits
    for (uint64_t mask = avail_ids; mask != 0; ) {
        const int cube_id = bitmask_first(mask);
        mask &= mask - 1; // Clear lowest set bit

        const std::vector<Cube>& cube_variants = variants_pos.variants[cube_id];
        for (const Cube& variant : cube_variants) {
            if (g_state->is_valid2(visible, variant)) {
                g_state->place_cube(visible, pos, cube_id, variant);

                if (pos <= DEPTH_TO_PRINT) {
                    sols += solve_from_pos(pos + 1);
                    auto elapsed = std::chrono::high_resolution_clock::now() - g_start_time;
                    auto elapsed_sec = std::chrono::duration_cast<std::chrono::milliseconds>(elapsed).count() / 1000.0;
                    std::cout << std::string(pos, '-') << " with " << variant.to_string()
                              << "\t" << std::fixed << std::setprecision(3) << elapsed_sec
                              << "s\t ";
                    std::cout.imbue(std::locale(""));
                    std::cout << sols;
                    std::cout.imbue(std::locale::classic());
                    std::cout << " solutions" << std::endl;
                } else {
                    sols += solve_from_pos_deep(pos + 1);
                }

                g_state->unplace_cube(visible, pos, cube_id, variant);
            }
        }
    }

    return sols;
}

uint64_t solve_from_pos_deep(int pos) {
    if (pos >= g_depth) [[unlikely]] {
        std::cout << g_state->to_string() << std::endl; // Print solution
        return 1;
    }

    const std::vector<int>& visible = g_state->visible[pos];
    SlotVariants& variants_pos = g_state->slot_cube_variants[pos];
    uint64_t sols = 0;

    const uint64_t avail_ids = bitmask_intersection(variants_pos.ids, g_state->available);

    for (uint64_t mask = avail_ids; mask != 0; ) {
        const int cube_id = bitmask_first(mask);
        mask &= mask - 1;

        const std::vector<Cube>& cube_variants = variants_pos.variants[cube_id];
        for (const Cube& variant : cube_variants) {
            if (g_state->is_valid2(visible, variant)) [[likely]] {
                g_state->place_cube(visible, pos, cube_id, variant);
                sols += solve_from_pos_deep(pos + 1);
                g_state->unplace_cube(visible, pos, cube_id, variant);
            }
        }
    }

    return sols;
}

uint64_t solve_sudoku_3d(Board* board, CubeCollection* cubes, int hint_cube_id = -1) {
    g_start_time = std::chrono::high_resolution_clock::now();
    g_depth = board->strip.size();

    State state(board, cubes);
    g_state = &state;

    // Force the first corner to always be the first piece
    SlotVariants& starting_corner = state.slot_cube_variants[0];
    int cube_id = bitmask_first(starting_corner.ids);
    const Cube& variant = starting_corner.variants[cube_id][0];
    const std::vector<int>& visible = state.visible[0];

    assert(state.is_valid2(visible, variant));
    state.place_cube(visible, 0, cube_id, variant);

    // If hint_cube_id is provided, place it at position 1 and start from position 2
    if (hint_cube_id >= 0) {
        const std::vector<int>& visible1 = state.visible[1];
        SlotVariants& variants_pos1 = state.slot_cube_variants[1];

        if (bitmask_contains(variants_pos1.ids, hint_cube_id) && bitmask_contains(state.available, hint_cube_id)) {
            const std::vector<Cube>& cube_variants = variants_pos1.variants[hint_cube_id];

            uint64_t sols = 0;

            // Try all valid variants and sum solutions
            for (const Cube& v : cube_variants) {
                if (state.is_valid2(visible1, v)) {
                    state.place_cube(visible1, 1, hint_cube_id, v);
                    std::cout << "Hint: initial corner cube pos[0]=" << state.piece[0].to_string() << " pos[1]=" << v.to_string() << std::endl;
                    sols += solve_from_pos(2);
                    state.unplace_cube(visible1, 1, hint_cube_id, v);
                }
            }

            if (sols == 0) {
                // All variants conflict
                std::cerr << "Conflict: initial corner cube pos[0]=" << state.piece[0].to_string() << " conflicts with hint cube #" << hint_cube_id << std::endl;
            }

            return sols;
        } else {
            std::cerr << "Warning: Hint cube #" << hint_cube_id << " is not valid for position 1" << std::endl;
            return 0;
        }
    }

    uint64_t sols = solve_from_pos(1);
    return sols;
}

int main(int argc, char* argv[]) {
    int hint_cube_id = -1;

    // Parse command-line arguments
    if (argc > 1) {
        hint_cube_id = std::atoi(argv[1]);
        if (hint_cube_id < 0 || hint_cube_id > 26) {
            std::cerr << "Invalid cube ID. Must be between 0 and 26." << std::endl;
            return 1;
        }
    }

    const int CUBE_LEN = 3;
    Board board(CUBE_LEN);

    // Canonical form: only marked face values (top, left, front)
    // Will be expanded to full 6-element arrays by CubeCollection
    std::vector<std::vector<int>> pieces = {
        // blank
        {}, // 0

        // one marked (top)
        {3}, // 1
        {4}, // 2
        {7}, // 3
        {8}, // 4
        {8}, // 5
        {9}, // 6

        // two marked (top, left)
        {1, 9}, // 7
        {3, 2}, // 8
        {7, 5}, // 9
        {4, 5}, // 10=A
        {4, 8}, // 11=B
        {5, 9}, // 12=C
        {6, 5}, // 13=D
        {7, 6}, // 14=E
        {3, 9}, // 15=F
        {7, 4}, // 16=G
        {7, 9}, // 17=H
        {4, 6}, // 18=I

        // three marked (top, left, front)
        {1, 3, 1}, // 19=J
        {7, 5, 3}, // 20=K
        {4, 2, 2}, // 21=L
        {9, 1, 2}, // 22=M
        {5, 8, 6}, // 23=N
        {8, 1, 8}, // 24=O
        {3, 1, 6}, // 25=P
        {2, 2, 6}, // 26=Q
    };

    assert(pieces.size() == CUBE_LEN * CUBE_LEN * CUBE_LEN);

    CubeCollection cubes(pieces);

    uint64_t sols = solve_sudoku_3d(&board, &cubes, hint_cube_id);
    std::cout << "Solutions found: " << sols << std::endl;

    return 0;
}
