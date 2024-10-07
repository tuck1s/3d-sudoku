
import copy

# Storage for solutions found
class Solutions:
    def __init__(self):
        self.found = []
        self.ping = 0
        self.iters = 0 # count iterations

    def rec_iter(self):
        self.iters += 1
        self.ping += 1
        if self.ping > 100000:
            print('.', end='', flush=True) # emit a progress "ping"
            self.ping = 0

    def add(self, board):
        size = len(board)
        for i, f in enumerate(self.found):
            same = True  # Start with the assumption that they are the same
            for x in range(size):
                for y in range(size):
                    for z in range(size):
                        if board[x][y][z] != f[x][y][z]:
                            same = False
                            break  # Exit the innermost loop
                    if not same:
                        break  # Exit the middle loop
                if not same:
                    break  # Exit the outer loop

            # If an identical match is found, we don't add the new board
            if same:
                print(f'duplicate of solution {i+1}')
                return

        # If no duplicates are found, add the new board to the list
        self.found.append(copy.deepcopy(board))

    def __len__(self):
        return len(self.found)