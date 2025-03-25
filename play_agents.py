import numpy as np
from collections import defaultdict
import random
import pickle
import pygame
import sys
from tic_tac_vis import setup, refresh, game as env

# Function to hash the game state into a unique, hashable representation
def hash_state(obs):
    """Convert observation to a hashable state for Q-table."""
    board_channel = obs[:, :, 0]  # Extract board state
    ages_channel = obs[:, :, 1]  # Extract ages of pieces
    board_str = ''.join(['X' if x == 1 else 'O' if x == -1 else ' ' for x in board_channel.flatten()])
    ages_str = ''.join(map(str, ages_channel.flatten().astype(int)))
    return (board_str, ages_str)

# Function to train Q-learning agents for both players (X and O)
def train_agents(episodes=1000, gamma=0.9, epsilon=1.0, decay_rate=0.99995, gui=True, visualize_every=100):
    """Train Q-learning agents for X and O with reward tracking and optional visualization."""
    Q_table_x = defaultdict(lambda: np.zeros(9))  # Q-table for player X
    Q_table_o = defaultdict(lambda: np.zeros(9))  # Q-table for player O
    total_actions = 9  # Total possible actions
    max_steps = 20  # Maximum steps per episode
    pygame_initialized = False  # Track if pygame is initialized

    # Variables to track rewards
    total_reward_x = 0.0
    total_reward_o = 0.0
    episode_rewards_x = []
    episode_rewards_o = []

    # Initialize GUI if enabled
    if gui:
        setup(GUI=True)
        pygame_initialized = True

    # Training loop for the specified number of episodes
    for episode in range(episodes):
        obs = env.reset()  # Reset the environment
        done = False
        step_count = 0
        current_epsilon = epsilon * (decay_rate ** episode)  # Decay epsilon for exploration
        visualize = gui and (episode % visualize_every == 0)  # Determine if visualization is needed
        episode_reward_x = 0.0
        episode_reward_o = 0.0
        starting_player = env.game.current_player  # Track the starting player

        # Print progress
        if visualize:
            print(f"Visualizing Episode {episode}/{episodes} (Starting Player: {starting_player})")
        elif episode % 1000 == 0:
            print(f"Training Episode {episode}/{episodes}")

        # Play one episode
        while not done and step_count < max_steps:
            legal_actions = env.get_legal_actions()  # Get legal actions
            if not legal_actions:
                break
            state_key = hash_state(obs)  # Hash the current state
            current_player = env.game.current_player  # Determine the current player
            Q_table = Q_table_x if current_player == 'X' else Q_table_o  # Select the appropriate Q-table

            # Choose action using epsilon-greedy policy
            if random.random() < current_epsilon:
                action = random.choice(legal_actions)  # Explore
            else:
                if state_key not in Q_table:
                    Q_table[state_key] = np.zeros(total_actions)  # Initialize Q-values
                action = max(legal_actions, key=lambda x: Q_table[state_key][x])  # Exploit

            # Take the action and observe the result
            next_obs, reward, done, info = env.step(action)
            info['action'] = action  # Add action info for visualization

            # Update rewards for the current player
            if current_player == 'X':
                episode_reward_x += reward
            else:
                episode_reward_o += reward

            # Visualize the game if enabled
            if visualize:
                refresh(next_obs, reward, done, info)

            # Update Q-table using the Q-learning formula
            next_state_key = hash_state(next_obs)
            if next_state_key not in Q_table:
                Q_table[next_state_key] = np.zeros(total_actions)
            learning_rate = 0.1
            current_q = Q_table[state_key][action]
            best_next_q = np.max(Q_table[next_state_key])
            Q_table[state_key][action] = (1 - learning_rate) * current_q + learning_rate * (reward + gamma * best_next_q)

            # Update the observation and step count
            obs = next_obs
            step_count += 1

            # Handle pygame events to allow quitting during visualization
            if visualize:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()

        # Track total rewards for both players
        total_reward_x += episode_reward_x
        total_reward_o += episode_reward_o
        episode_rewards_x.append(episode_reward_x)
        episode_rewards_o.append(episode_reward_o)

        # Print summary at the end of training
        if episode == episodes - 1:
            print(f"\nTraining Complete!")
            print(f"Total Reward for X: {total_reward_x:.2f}")
            print(f"Total Reward for O: {total_reward_o:.2f}")
            avg_reward_x = np.mean(episode_rewards_x) if episode_rewards_x else 0.0
            avg_reward_o = np.mean(episode_rewards_o) if episode_rewards_o else 0.0
            print(f"Average Reward per Episode for X: {avg_reward_x:.4f}")
            print(f"Average Reward per Episode for O: {avg_reward_o:.4f}")

    # Save Q-tables to files
    with open('Q_table_x.pkl', 'wb') as f:
        pickle.dump(dict(Q_table_x), f)
    with open('Q_table_o.pkl', 'wb') as f:
        pickle.dump(dict(Q_table_o), f)

    # Quit pygame if it was initialized
    if pygame_initialized:
        pygame.quit()
    
    return Q_table_x, Q_table_o

# Function to play a single game using trained Q-tables
def play_game(Q_table_x, Q_table_o, gui=True, max_steps=20):
    """Play a single game with trained agents, optionally with GUI."""
    if gui:
        setup(GUI=True)  # Initialize GUI

    obs = env.reset()  # Reset the environment
    done = False
    step_count = 0
    starting_player = env.game.current_player  # Track the starting player
    print(f"Final Game (Starting Player: {starting_player})")

    # Play the game until it's done or max steps are reached
    while not done and step_count < max_steps:
        legal_actions = env.get_legal_actions()  # Get legal actions
        if not legal_actions:
            break
        state_key = hash_state(obs)  # Hash the current state
        current_player = env.game.current_player  # Determine the current player
        Q_table = Q_table_x if current_player == 'X' else Q_table_o  # Select the appropriate Q-table

        # Choose the best action based on the Q-table
        if state_key not in Q_table:
            Q_table[state_key] = np.zeros(9)  # Initialize Q-values
        action = max(legal_actions, key=lambda x: Q_table[state_key][x])

        # Take the action and observe the result
        next_obs, reward, done, info = env.step(action)
        info['action'] = action  # Add action info for visualization
        if gui:
            refresh(next_obs, reward, done, info)  # Visualize the game

        # Update the observation and step count
        obs = next_obs
        step_count += 1

        # Handle pygame events to allow quitting during visualization
        if gui:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

    # Keep the GUI open after the game ends
    if gui:
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

# Main entry point for training and playing the game
if __name__ == "__main__":
    print("Training agents with visualization every 100 episodes and random starting players...")
    Q_table_x, Q_table_o = train_agents(episodes=1000, gui=False, visualize_every=100)
    print("Playing a game with trained agents (GUI enabled)...")
    play_game(Q_table_x, Q_table_o, gui=True)