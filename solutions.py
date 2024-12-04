
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

    def add(self, state:State):
        self.rec_iter()
        print(state)
        sol = tuple(state.piece)
        if sol in self.found:
            print(f'duplicate solution')
        else:
            self.found.add(sol)

    def __len__(self):
        return len(self.found)