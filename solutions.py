
from board import Board, State
import sys, time

# Storage for solutions found
class Solutions:
    def __init__(self, board:Board):
        self.board = board
        self.found = set()
        self.ping = 0
        self.iters = 0 # count iterations
        self.ping2 = 0
        self.ping2_time = time.time()

    # Progress comfort reporting and execution time output on stderr
    def rec_iter(self):
        self.iters += 1
        self.ping += 1
        if self.ping > 1000:
            print('.', file=sys.stderr, end='', flush=True) # emit a progress "ping"
            self.ping = 0
            self.ping2 += 1
            if self.ping2 > 100:
                end_time = time.time()
                elapsed_time = end_time - self.ping2_time
                self.ping2_time = end_time
                print(f'\n{elapsed_time:.3f} seconds', file=sys.stderr)
                self.ping2 = 0

    # use set to dedup results
    def add(self, state:State):
        t = tuple(state.piece)
        if not t in self.found:
            self.rec_iter()
            if t in self.found:
                print('Duplicate')
            else:
                self.found.add(t) # Store as a tuple so it's hashable

    def __len__(self):
        return len(self.found)

    def dump(self):
        for s in self.found:
            # Reassemble the State from the tuple
            state = State(self.board)
            state.piece = list(s)
            print(state)