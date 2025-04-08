# Checkers
# 🧠 Checkers Game with AI (Pygame + Minimax)

A full-featured Checkers (Draughts) game built with Python and Pygame, featuring a human vs AI gameplay experience. The AI opponent is powered by a custom-designed heuristic function and the Minimax algorithm with alpha-beta pruning for optimized decision-making.

---

## 🎮 Features

- ✅ Fully playable Checkers game with GUI
- 🧠 Intelligent AI opponent using Minimax + Alpha-Beta pruning
- 🎯 Custom heuristic function designed for strategic play
- 🔁 Turn-based logic with legal move validation
- 💥 Piece capturing and multi-capture logic
- 👑 King promotion with backward moves
- 📦 Built with Pygame for smooth rendering and user interaction

---

## 🛠️ Technologies Used

- **Python 3.11**
- **Pygame** – for game loop, rendering, and event handling
- **Minimax Algorithm** – AI decision-making
- **Alpha-Beta Pruning** – optimization of Minimax
- **Custom Heuristics** – to evaluate game board states

---

## 🤖 AI Logic

The AI opponent uses the **Minimax algorithm** with **alpha-beta pruning**, allowing it to simulate and evaluate potential future moves efficiently.

### 🔍 Heuristic Function Includes:
- Material advantage (number of pieces)
- King weighting (king > pawn)
- Central control of the board
- Safe pieces (non-capturable)
- Potential moves (mobility)
- Aggressiveness vs. defensiveness balance

### 🧠 Minimax with Alpha-Beta:
- Recursively evaluates possible moves up to a certain depth
- Prunes unnecessary branches using alpha and beta values
- Reduces computation time significantly without sacrificing performance

---

## 🚀 Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/nikola0234/Checkers
cd checkers-ai
pip install pygame
python3 main.py

