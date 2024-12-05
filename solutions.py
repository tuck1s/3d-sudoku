
from board import Board, State
import sys, time

# Storage for solutions found
class Solutions:
    def __init__(self, board:Board):
        self.board = board
        self.found = set()
        self.ping = 0
        self.ping_time = time.time()
        self.total = 0

    # Progress comfort reporting and execution time output on stderr
    def rec_iter(self):
        self.total += 1
        self.ping += 1
        if self.ping >= 100000:
            self.ping = 0
            end_time = time.time()
            elapsed_time = end_time - self.ping_time
            self.ping_time = end_time
            print(f'\n{elapsed_time:.3f} seconds, {self.total} solutions so far', file=sys.stderr)

    # use set to dedup results
    def add(self, state:State):
        # t = tuple(state.piece)
        if self.total == 0:
            print('First solution found:')
            print(state)
        self.rec_iter()
            #if t in self.found:
            #   print('Duplicate')
            #else:
                # print(state)
                # self.found.add(t) # Store as a tuple so it's hashable

    def __len__(self):
        return len(self.found)

    def dump(self):
        for s in self.found:
            # Reassemble the State from the tuple
            state = State(self.board)
            state.piece = list(s)
            print(state)