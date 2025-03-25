import numpy as np
import random

class EphemeralTicTacToe:
    def __init__(self, grid_size=3, lifespan_x=6, lifespan_o=6):
        self.grid_size = grid_size
        self.lifespan_x = lifespan_x
        self.lifespan_o = lifespan_o
        self.reset()

    def reset(self, starting_player=None):
        self.board = np.full((self.grid_size, self.grid_size), None, dtype=object)
        self.ages = np.zeros((self.grid_size, self.grid_size), dtype=int)
        self.owners = np.full((self.grid_size, self.grid_size), None, dtype=object)
        self.current_player = random.choice(['X', 'O']) if starting_player is None else starting_player
        self.move_count = 0
        return self.get_state()

    def get_state(self):
        return (self.board.copy(), self.ages.copy(), self.current_player, self.owners.copy())

    def step(self, action):
        row, col = action
        if self.board[row, col] is not None:
            return self.get_state(), -0.1, False

        self.move_count += 1

        for i in range(self.grid_size):
            for j in range(self.grid_size):
                if self.board[i, j] is not None:
                    self.ages[i, j] += 1

        for i in range(self.grid_size):
            for j in range(self.grid_size):
                if self.board[i, j] is not None:
                    if self.owners[i, j] == 'X' and self.ages[i, j] >= self.lifespan_x:
                        print(f"Expiring X at ({i}, {j}), Age: {self.ages[i, j]}")
                        self.board[i, j] = None
                        self.ages[i, j] = 0
                        self.owners[i, j] = None
                    elif self.owners[i, j] == 'O' and self.ages[i, j] >= self.lifespan_o:
                        print(f"Expiring O at ({i}, {j}), Age: {self.ages[i, j]}")
                        self.board[i, j] = None
                        self.ages[i, j] = 0
                        self.owners[i, j] = None

        self.board[row, col] = self.current_player
        self.ages[row, col] = 0
        self.owners[row, col] = self.current_player

        print(f"Move {self.move_count}, Ages:\n{self.ages}")
        print(f"Board after move {self.move_count}:\n{self.board}")

        if self.check_win(self.current_player):
            return self.get_state(), 1, True

        self.current_player = 'O' if self.current_player == 'X' else 'X'
        if not self.get_legal_actions():
            return self.get_state(), 0, True

        return self.get_state(), 0, False

    def check_win(self, player):
        for i in range(self.grid_size):
            if all(self.board[i, j] == player for j in range(self.grid_size)) or \
               all(self.board[j, i] == player for j in range(self.grid_size)):
                return True
        if all(self.board[i, i] == player for i in range(self.grid_size)) or \
           all(self.board[i, self.grid_size - 1 - i] == player for i in range(self.grid_size)):
            return True
        return False

    def get_legal_actions(self):
        return [(i, j) for i in range(self.grid_size) for j in range(self.grid_size) 
                if self.board[i, j] is None]