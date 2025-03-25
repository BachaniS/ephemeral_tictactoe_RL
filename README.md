# 🎮 Ephemeral Tic-Tac-Toe: The Ever-Changing Battle!

**An AI-powered, reinforcement-learning-enhanced twist on the classic Tic-Tac-Toe, where pieces have a lifespan!**

## 🚀 What is Ephemeral Tic-Tac-Toe?
This isn't your childhood Tic-Tac-Toe. Here, pieces **expire** after a set number of turns! That means strategies evolve, moves are temporary, and winning requires outlasting your opponent. Plus, we've got **Q-learning** AI agents that get smarter over time! 🧠🤖

## 🎯 Features
✔ **Dynamic Gameplay** – Pieces vanish after a set number of turns, keeping things fresh!
✔ **Reinforcement Learning** – AI agents learn how to master the game using Q-learning. 🏆
✔ **Gym Environment** – Fully compatible with OpenAI Gym for easy RL experimentation.
✔ **Visualized with Pygame** – Watch the game unfold with a slick GUI! 🎨
✔ **Customizable Lifespans** – Adjust how long Xs and Os survive before disappearing.

## 🏗️ Project Structure
```
📂 ephemeral-tic-tac-toe
├── mdp_gym.py          # Game logic with ephemeral piece mechanics
├── tic_tac_env.py      # Gym environment wrapper for AI training
├── tic_tac_vis.py      # Pygame-powered visualization
├── play_agents.py      # Q-learning training & agent gameplay
├── README.md           # You're reading it now! 📖
```

## 🎲 How to Play
1️⃣ Run the game in visualization mode:
```bash
python tic_tac_vis.py
```
2️⃣ Train AI agents:
```bash
python play_agents.py
```
3️⃣ Watch trained agents battle it out:
```bash
python play_agents.py --play
```

## 🏗️ Training the AI
The AI agents use **Q-learning** with an epsilon-greedy strategy. They get better over time by maximizing rewards and learning from past moves. You can tweak training settings like **episodes, epsilon decay, and gamma** in `play_agents.py`.

## 🎨 Game Visualization
Want to see the game in action? Pygame brings it to life! The board updates dynamically as pieces age and disappear. Customize colors, speeds, and visuals in `tic_tac_vis.py`.

## ⚡ Future Enhancements
🔹 Train deep reinforcement learning models (DQN) for advanced AI.
🔹 Implement multiplayer support (local or online). 🎭
🔹 Add different board sizes and lifespans for more complexity.

## 📜 License
MIT License – because knowledge (and code) should be shared! 🚀

## 🤝 Contributions
Found a bug? Have a cool idea? PRs welcome! Let's make ephemeral Tic-Tac-Toe even more epic. 💡

