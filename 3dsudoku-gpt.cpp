#include <iostream>
#include <vector>
#include <array>
#include <cassert>
#include <chrono>
#include <iomanip>

// Sides enum
enum Sides { TOP=0, BOTTOM=1, LEFT=2, RIGHT=3, FRONT=4, BACK=5 };

// Marks enum
enum Marks { CENTRE=0, FACE=1, EDGE=2, CORNER=3 };

// Bitmask utilities
inline bool bitmask_contains(uint64_t mask, int val) { return (mask & (1ull<<val)) != 0; }
inline void bitmask_add(uint64_t& mask, int val) { mask |= (1ull<<val); }
inline void bitmask_remove(uint64_t& mask, int val) { mask &= ~(1ull<<val); }
inline uint64_t bitmask_intersection(uint64_t a, uint64_t b) { return a & b; }
inline int bitmask_popcount(uint64_t mask) { return __builtin_popcountll(mask); }
inline int bitmask_first(uint64_t mask) { return mask==0?-1:__builtin_ctzll(mask); }

// Cube class
class Cube {
public:
    std::array<int,6> faces;
    int id;
    Cube() : id(-1) { faces.fill(0); }
    Cube(const std::array<int,6>& f, int cube_id) : faces(f), id(cube_id) {}
    int nonblanks() const { int c=0; for(int f:faces) if(f>0) c++; return c; }
    bool operator==(const Cube& o) const { return faces==o.faces; }
    bool operator!=(const Cube& o) const { return !(*this==o); }
    std::string to_string() const {
        std::string r;
        for(int f:faces) r += (f>0?std::to_string(f):"-")+" ";
        if(!r.empty()) r.pop_back();
        return r;
    }
};

// 6/9 ambiguity
Cube alternate_69(const Cube& c){
    static const int swap[]={0,1,2,3,4,5,9,7,8,6};
    std::array<int,6> alt;
    for(int i=0;i<6;i++) alt[i]=swap[c.faces[i]];
    return Cube(alt,c.id);
}

// Cube rotations (24)
std::vector<Cube> rotations(const Cube& c){
    static const int face_mappings[24][6] = {
        {0,1,2,3,4,5},{0,1,4,5,3,2},{0,1,3,2,5,4},{0,1,5,4,2,3},
        {1,0,3,2,4,5},{1,0,4,5,2,3},{1,0,2,3,5,4},{1,0,5,4,3,2},
        {2,3,0,1,5,4},{2,3,5,4,1,0},{2,3,1,0,4,5},{2,3,4,5,0,1},
        {3,2,1,0,5,4},{3,2,5,4,0,1},{3,2,0,1,4,5},{3,2,4,5,1,0},
        {4,5,2,3,1,0},{4,5,1,0,3,2},{4,5,3,2,0,1},{4,5,0,1,2,3},
        {5,4,3,2,1,0},{5,4,1,0,2,3},{5,4,2,3,0,1},{5,4,0,1,3,2}
    };
    std::vector<std::array<int,6>> uniq;
    for(int m=0;m<24;m++){
        std::array<int,6> o;
        for(int i=0;i<6;i++) o[i]=c.faces[face_mappings[m][i]];
        bool found=false;
        for(auto &e:uniq) if(e==o){found=true;break;}
        if(!found) uniq.push_back(o);
    }
    std::vector<Cube> res; for(auto &f:uniq) res.emplace_back(f,c.id); return res;
}

// All cube variants (rotations + 6/9)
std::vector<Cube> get_variants(const Cube& c){
    std::vector<Cube> v = rotations(c);
    Cube alt = alternate_69(c);
    if(alt!=c){
        std::vector<Cube> alt_rots = rotations(alt);
        v.insert(v.end(), alt_rots.begin(), alt_rots.end());
    }
    return v;
}

// CubeCollection
class CubeCollection{
public:
    std::array<std::vector<Cube>,4> marked_cubes;
    CubeCollection(const std::vector<std::array<int,6>>& fl){
        for(int id=0;id<fl.size();id++){
            Cube c(fl[id],id);
            int marks=c.nonblanks();
            marked_cubes[marks].push_back(c);
        }
    }
};

// BoardSlot
class BoardSlot{ public: uint64_t sides_touched; BoardSlot(uint64_t s):sides_touched(s){}; };

// Board
class Board{
public:
    int size; std::vector<std::vector<std::vector<int>>> grid; std::vector<BoardSlot> strip;
    Board(int sz):size(sz){
        grid.resize(sz,std::vector<std::vector<int>>(sz,std::vector<int>(sz,-1)));
        auto get_sides=[sz](int i,Sides start,Sides end)->uint64_t{
            uint64_t m=0;
            if(i==0) bitmask_add(m,start);
            else if(i==sz-1) bitmask_add(m,end);
            return m;
        };
        for(int z=0;z<sz;z++) for(int y=0;y<sz;y++) for(int x=0;x<sz;x++){
            uint64_t m = get_sides(x,LEFT,RIGHT)|get_sides(y,BACK,FRONT)|get_sides(z,BOTTOM,TOP);
            strip.emplace_back(m);
            grid[x][y][z]=strip.size()-1;
        }
    }
};

// SlotVariants
class SlotVariants{
public:
    std::vector<std::vector<Cube>> variants; uint64_t ids;
    SlotVariants():ids(0){variants.resize(27);}
    void add(const Cube& c,const std::vector<Cube>& v_list){variants[c.id]=v_list; bitmask_add(ids,c.id);}
};

// State
class State{
public:
    Board* board;
    std::array<uint64_t,6> sides;
    std::vector<Cube> piece;
    uint64_t available;
    std::vector<std::vector<int>> visible;
    std::vector<SlotVariants> slot_cube_variants;

    State(Board* b, CubeCollection* cubes):board(b){
        sides.fill(0); piece.resize(board->strip.size()); available=0;
        visible.resize(board->strip.size()); slot_cube_variants.resize(board->strip.size());

        for(int i=0;i<board->strip.size();i++){
            uint64_t s=board->strip[i].sides_touched;
            for(int f=0;f<6;f++) if(bitmask_contains(s,f)) visible[i].push_back(f);
        }

        for(int marks=0;marks<4;marks++){
            for(const Cube& c:cubes->marked_cubes[marks]){
                bitmask_add(available,c.id);
                std::vector<Cube> vars=get_variants(c);
                for(int i=0;i<visible.size();i++){
                    if(visible[i].size()==marks){
                        std::vector<Cube> valid;
                        for(const Cube& v:vars) {
                            bool ok=true; for(int f:visible[i]) if(v.faces[f]==0){ok=false;break;}
                            if(ok) valid.push_back(v);
                        }
                        if(!valid.empty()) slot_cube_variants[i].add(c,valid);
                    }
                }
            }
        }
    }

    void place_cube(const std::vector<int>& vis,int pos,int cube_id,const Cube& v){
        bitmask_remove(available,cube_id); piece[pos]=v; for(int f:vis) bitmask_add(sides[f],v.faces[f]);
    }
    void unplace_cube(const std::vector<int>& vis,int pos,int cube_id,const Cube& v){
        bitmask_add(available,cube_id); piece[pos]=Cube(); for(int f:vis) bitmask_remove(sides[f],v.faces[f]);
    }
    bool is_valid2(const std::vector<int>& vis,const Cube& v) const{
        for(int f:vis) if(bitmask_contains(sides[f],v.faces[f])) return false;
        return true;
    }
};

// Globals
State* g_state=nullptr; int g_depth=0;
auto g_start_time=std::chrono::high_resolution_clock::now();

// Solver forward
int solve_from_pos(int pos);
int solve_from_pos_deep(int pos);

int solve_from_pos(int pos){
    const auto& visible=g_state->visible[pos];
    SlotVariants& sv=g_state->slot_cube_variants[pos];
    int sols=0;
    uint64_t avail=bitmask_intersection(sv.ids,g_state->available);
    for(uint64_t mask=avail;mask!=0;){
        int cid=bitmask_first(mask); mask &= mask-1;
        for(const Cube& v:sv.variants[cid]){
            if(g_state->is_valid2(visible,v)){
                g_state->place_cube(visible,pos,cid,v);
                if(pos<=8){
                    sols += solve_from_pos(pos+1);
                    auto elapsed = std::chrono::high_resolution_clock::now()-g_start_time;
                    double sec = std::chrono::duration_cast<std::chrono::milliseconds>(elapsed).count()/1000.0;
                    std::cout << std::string(pos,'-') << " with " << v.to_string() 
                              << "\t" << std::fixed << std::setprecision(3) << sec 
                              << "s\t " << sols << " solutions" << std::endl;
                } else sols += solve_from_pos_deep(pos+1);
                g_state->unplace_cube(visible,pos,cid,v);
            }
        }
    }
    return sols;
}

int solve_from_pos_deep(int pos){
    if(pos>=g_depth) return 1;
    const auto& visible=g_state->visible[pos];
    SlotVariants& sv=g_state->slot_cube_variants[pos];
    int sols=0;
    uint64_t avail=bitmask_intersection(sv.ids,g_state->available);
    for(uint64_t mask=avail;mask!=0;){
        int cid=bitmask_first(mask); mask&=mask-1;
        for(const Cube& v:sv.variants[cid]){
            if(g_state->is_valid2(visible,v)){
                g_state->place_cube(visible,pos,cid,v);
                sols += solve_from_pos_deep(pos+1);
                g_state->unplace_cube(visible,pos,cid,v);
            }
        }
    }
    return sols;
}

int solve_sudoku_3d(Board* board, CubeCollection* cubes){
    g_start_time=std::chrono::high_resolution_clock::now();
    g_depth=board->strip.size();
    State state(board,cubes);
    g_state=&state;

    // force first corner
    SlotVariants& start=state.slot_cube_variants[0];
    int cid=bitmask_first(start.ids);
    const Cube& v=start.variants[cid][0];
    const auto& visible=state.visible[0];
    state.place_cube(visible,0,cid,v);

    return solve_from_pos(1);
}

int main(){
    const int CUBE_LEN=3;
    Board board(CUBE_LEN);
    std::vector<std::array<int,6>> pieces={
        {0,0,0,0,0,0},
        {3,0,0,0,0,0},{4,0,0,0,0,0},{7,0,0,0,0,0},{8,0,0,0,0,0},{8,0,0,0,0,0},{9,0,0,0,0,0},
        {1,0,0,0,9,0},{3,0,0,0,2,0},{7,0,0,5,0,0},{4,0,0,5,0,0},{4,0,0,0,0,8},{5,0,0,9,0,0},{6,0,0,5,0,0},{7,0,0,0,0,6},{3,0,0,0,9,0},{7,0,0,4,0,0},{7,0,0,0,9,0},{4,0,0,0,0,6},
        {1,0,3,0,1,0},{7,0,0,3,5,0},{4,0,2,0,2,0},{9,0,2,0,0,1},{5,0,6,0,0,8},{8,0,0,1,0,8},{3,0,1,0,6,0},{2,0,0,6,2,0}
    };
    assert(pieces.size()==CUBE_LEN*CUBE_LEN*CUBE_LEN);
    CubeCollection cubes(pieces);
    int sols = solve_sudoku_3d(&board,&cubes);
    std::cout << "Solutions found: " << sols << std::endl;
    return 0;
}
