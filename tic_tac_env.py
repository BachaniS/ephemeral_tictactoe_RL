import gym
from gym import spaces
import numpy as np
from mdp_gym import EphemeralTicTacToe

class EphemeralTicTacToeEnv(gym.Env):
    def __init__(self, grid_size=3, lifespan_x=6, lifespan_o=6):
        super(EphemeralTicTacToeEnv, self).__init__()
        self.game = EphemeralTicTacToe(grid_size, lifespan_x, lifespan_o)
        self.grid_size = grid_size
        self.action_space = spaces.Discrete(grid_size * grid_size)
        self.observation_space = spaces.Box(low=-1, high=max(lifespan_x, lifespan_o), 
                                           shape=(self.grid_size, self.grid_size, 3), dtype=np.float32)

    def reset(self):
        state = self.game.reset()  # No starting_player parameter unless explicitly needed
        return self._get_observation(state)

    def step(self, action):
        row, col = divmod(action, self.grid_size)
        legal_actions = self.get_legal_actions()
        if action not in legal_actions:
            return self._get_observation(self.game.get_state()), -0.1, False, {"reason": "illegal move"}
        
        state, reward, done = self.game.step((row, col))
        return self._get_observation(state), reward, done, {"action": (row, col)}

    def _get_observation(self, state):
        board, ages, _, owners = state
        obs = np.zeros((self.grid_size, self.grid_size, 3), dtype=np.float32)
        for i in range(self.grid_size):
            for j in range(self.grid_size):
                if board[i, j] == 'X':
                    obs[i, j, 0] = 1
                elif board[i, j] == 'O':
                    obs[i, j, 0] = -1
                obs[i, j, 1] = ages[i, j]
                if owners[i, j] == 'X':
                    obs[i, j, 2] = 1
                elif owners[i, j] == 'O':
                    obs[i, j, 2] = -1
        return obs

    def get_legal_actions(self):
        return [i * self.grid_size + j for i, j in self.game.get_legal_actions()]