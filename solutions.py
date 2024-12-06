
from board import Board, State
import sys, time

# Storage for solutions found
class Solutions:
    def __init__(self, board:Board):
        self.board = board
        self.ping = 0
        self.ping_time = time.time()
        self.total = 0

    # Progress comfort reporting and execution time output on stderr
    def add(self, state:State):
        if self.total == 0:
            print('First solution found:')
            print(state)

        self.total += 1
        self.ping += 1
        if self.ping >= 1000000:
            self.ping = 0
            end_time = time.time()
            elapsed_time = end_time - self.ping_time
            self.ping_time = end_time
            print(f'{elapsed_time:.3f} seconds, {self.total:,} solutions so far', file=sys.stderr)
