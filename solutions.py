
from board import State

# Storage for solutions found
class Solutions:
    def __init__(self):
        self.found = set()
        self.ping = 0
        self.iters = 0 # count iterations

    def rec_iter(self):
        self.iters += 1
        self.ping += 1
        if self.ping > 1000:
            print('.', end='', flush=True) # emit a progress "ping"
            self.ping = 0

    # use set to dedup results
    def add(self, state:State):
        self.rec_iter()
        sol = tuple(state.piece)
        self.found.add(sol)

    def __len__(self):
        return len(self.found)