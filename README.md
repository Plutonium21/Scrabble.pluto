# Scrabble.pluto

**An AI-powered implementation of Scrabble using Trie-based word generation, anchor-driven move search, and a greedy heuristic evaluation strategy.**

[![Python](https://img.shields.io/badge/Python-3.12-blue.svg)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/UI-Streamlit-FF4B4B.svg)](https://streamlit.io/)
[![Course](https://img.shields.io/badge/Course-CSD311-purple.svg)](#)

> **Live Application:** https://scrabble-pluto.streamlit.app
> **GitHub Repository:** https://github.com/Plutonium21/Scrabble.pluto

---

## Overview

**Scrabble.pluto** is a Python-based implementation of the classic word game Scrabble, developed as a course project for **CSD311 – Artificial Intelligence**.

The project combines a functional Scrabble game engine with an AI opponent capable of generating and evaluating legal moves. Rather than checking every possible word at every board position, the AI uses an **anchor-driven move generation strategy** supported by a **Trie (prefix tree)** to efficiently explore valid word combinations.

A greedy heuristic evaluates the generated moves and selects the move with the highest estimated value.

The application provides an interactive interface built with Streamlit, allowing a human player to compete against the AI.

## Key Features

- **Interactive Scrabble gameplay:** Play against an AI opponent through a Streamlit interface.
- **Trie-based dictionary:** Stores valid words in a prefix tree for efficient prefix and word lookup.
- **Anchor-driven move generation:** Restricts move exploration to strategically relevant board positions.
- **Recursive Trie traversal:** Generates candidate words by traversing the Trie while accounting for existing board tiles and available rack tiles.
- **Blank tile support:** Handles blank tiles as zero-value tiles that can represent any alphabetic character.
- **Move validation:** Checks candidate moves against Scrabble placement and word-validity rules.
- **Scoring engine:** Accounts for letter premiums, word premiums, cross-words, and bingo bonuses.
- **Greedy heuristic evaluation:** Selects a move using immediate score and a small rack-utilisation bonus.
- **Modular architecture:** Separates the game engine, AI logic, and user interface.

---

## AI Algorithm

The AI follows a **generate → validate → evaluate → select** pipeline.

### 1. Trie-Based Dictionary

The dictionary is stored in a Trie data structure.

Each Trie node contains:
- A dictionary of child nodes representing possible next characters.
- A Boolean flag indicating whether the current node represents the end of a valid word.

This allows the AI to:
- Check whether a complete word exists.
- Check whether a sequence of characters is a valid prefix.
- Prune recursive search paths as soon as they no longer match any dictionary word.

The Trie is constructed from the project's wordlist during application initialisation and cached for reuse.

### 2. Anchor-Driven Move Generation

Instead of attempting to place words at every possible board coordinate, the move generator identifies **anchor squares**.

An anchor is an empty square adjacent to an existing tile horizontally or vertically. On an empty board, the centre square is used as the initial anchor.

The move generator uses these anchors to identify relevant starting positions and explore placements that connect to the existing board.

This reduces unnecessary search and ensures that generated moves can connect to the current game.

### 3. Recursive Trie-Guided Search

The move generator recursively explores possible word placements while traversing the Trie.

During traversal, it:
- Follows existing board letters when a position is already occupied.
- Tries available rack letters at empty positions.
- Explores alternative letters when a blank tile is available.
- Stops exploring a branch when the corresponding Trie prefix does not exist.
- Records completed candidate words that satisfy the anchor requirement.

Generated candidates are subsequently checked by the game rules engine, and duplicate moves are removed.

### 4. Move Validation and Scoring

Each candidate move is passed through the rules engine before being considered by the AI.

Validation includes:
- Board boundaries and placement direction.
- Rack tile availability.
- Compatibility with existing board tiles.
- Connection to the existing board.
- Validity of the main word and perpendicular cross-words.

The scoring engine calculates the move's points using:
- Letter values.
- Double Letter and Triple Letter squares.
- Double Word and Triple Word squares.
- Perpendicular words formed by the placement.
- The 50-point bonus for using all seven rack tiles.

### 5. Greedy Heuristic Evaluation

The AI uses a greedy, one-ply heuristic to rank legal candidate moves.

The evaluation function is:

\[
H(m) = S(m) + 0.20 \times U(m)
\]

Where:

- \(H(m)\) = heuristic value of move \(m\).
- \(S(m)\) = immediate Scrabble score of the move.
- \(U(m)\) = number of rack tile indices used by the move.

The AI selects:

\[
m^* = \arg\max_{m \in M} H(m)
\]

Where \(M\) is the set of generated and validated legal moves.

This strategy prioritises immediate scoring while providing a small preference for moves that use more rack tiles.

**Important:** This is a greedy heuristic-based AI, not a trained machine learning model, minimax search, or reinforcement learning agent. It evaluates the immediate value of generated moves rather than simulating future turns.

---

## Project Architecture

The project follows a modular structure:

```text
Scrabble.pluto/
│
├── app.py
├── requirements.txt
├── README.md
├── pytest.ini
│
├── ai/
│   ├── evaluator.py
│   ├── move_generator.py
│   ├── trie.py
│   └── __init__.py
│
├── engine/
│   ├── board.py
│   ├── constants.py
│   ├── dictionary.py
│   ├── game_state.py
│   ├── rules.py
│   ├── scoring.py
│   ├── tile.py
│   ├── tile_bag.py
│   └── __init__.py
│
├── ui/
│   ├── app.py
│   └── app_diagnosticver.py
│
├── data/
│   ├── README.txt
│   └── words.txt
│
├── tests/
│   ├── test_ai.py
│   ├── test_board.py
│   ├── test_rules.py
│   ├── test_scoring.py
│   └── test_trie.py
│
├── benchmark_ai.py
└── diagnostic.py
```

### Module Responsibilities

| Module | Responsibility |
|---|---|
| `app.py` | Root Streamlit launcher |
| `ui/` | Interactive game interface and turn management |
| `ai/trie.py` | Trie data structure and dictionary traversal |
| `ai/move_generator.py` | Anchor-based recursive candidate generation |
| `ai/evaluator.py` | Greedy heuristic and move selection |
| `engine/board.py` | Board representation and premium squares |
| `engine/constants.py` | Tile values and tile distribution |
| `engine/tile.py` | Tile representation |
| `engine/tile_bag.py` | Tile distribution, shuffling, drawing, and exchange |
| `engine/dictionary.py` | Wordlist loading and dictionary lookup |
| `engine/rules.py` | Move validation and placement |
| `engine/scoring.py` | Scrabble scoring calculations |
| `engine/game_state.py` | Turn management, racks, scores, history, and endgame state |
| `data/` | Dictionary and associated data documentation |
| `tests/` | Automated tests for game and AI components |
| `benchmark_ai.py` | AI performance benchmarking |
| `diagnostic.py` | Project diagnostic utilities |

---

## Technology Stack

| Technology | Purpose |
|---|---|
| Python 3.12 | Core implementation |
| Streamlit | Interactive web application |
| Trie | Efficient dictionary prefix traversal |
| Recursive search | Candidate move generation |
| Greedy heuristic | AI move evaluation and selection |
| Pytest | Automated testing |
| Git and GitHub | Version control and project hosting |
| Streamlit Community Cloud | Application deployment |

---

## Installation and Local Setup

### Prerequisites

- Python 3.12
- Git
- pip

### 1. Clone the repository

```bash
git clone https://github.com/Plutonium21/Scrabble.pluto.git
cd Scrabble.pluto
```

### 2. Create a virtual environment

**Windows (PowerShell):**

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```

**Linux / macOS:**

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Launch the application

Run the following command from the repository root:

```bash
streamlit run app.py
```

The application will be available at the local URL displayed in the terminal, usually:

```text
http://localhost:8501
```

**Note:** Run the application from the repository root. The root `app.py` launches `ui/app.py`, and the dictionary loader expects the data directory to be available relative to the project root.

---

## Testing

The project includes automated tests covering the core game engine and AI components.

Run the test suite from the repository root:

```bash
pytest -q
```

To run individual test modules:

```bash
pytest tests/test_trie.py -v
pytest tests/test_ai.py -v
pytest tests/test_rules.py -v
pytest tests/test_scoring.py -v
pytest tests/test_board.py -v
```

---

## Performance Benchmarking

The project includes `benchmark_ai.py` to measure dictionary loading, Trie construction, and move-generation performance on different board states.

Previously recorded local benchmark measurements:

| Metric | Recorded Result |
|---|---:|
| Dictionary loading | 0.563 s |
| Trie construction | 3.498 s |
| Opening-position legal moves | 342 |
| Opening-position average generation time | 0.0313 s |
| Early-game legal moves | 418 |
| Early-game average generation time | 0.2116 s |

These measurements were recorded on the development machine and are hardware- and environment-dependent. They should not be interpreted as guaranteed performance on the deployed application.

To run the benchmark:

```bash
python benchmark_ai.py
```

---

## Deployment

The application is intended to be hosted using **Streamlit Community Cloud**.

Deployment configuration:

| Setting | Value |
|---|---|
| Repository | `Plutonium21/Scrabble.pluto` |
| Branch | `main` |
| Main file path | `app.py` |
| Python version | `3.12` |

**Live application:** [https://scrabble-pluto.streamlit.app](https://scrabble-pluto.streamlit.app)

---

## Current Scope and Limitations

The current AI uses a greedy, one-ply heuristic. It selects the highest-valued move from the legal candidates generated for the current board state.

The current evaluation function does not explicitly model:
- Opponent responses.
- Future board states.
- Long-term rack leave quality.
- Strategic denial of premium squares.
- Probability-based endgame planning.

These provide opportunities for future development.

### Potential Future Improvements

- Multi-ply search with minimax or expectimax.
- Alpha-beta pruning.
- Improved rack-leave evaluation.
- Strategic premium-square control.
- Board-position-aware heuristic features.
- More extensive AI benchmarking across different game states.

---

## Wordlist and Data Attribution

The project uses the wordlist supplied with the project under `data/words.txt`.

The list was obtained through the following community discussion:

[2019 Collins Scrabble Words List in Text File – Board & Card Games Stack Exchange](https://boardgames.stackexchange.com/questions/38366/latest-collins-scrabble-words-list-in-text-file)

The accompanying `data/README.txt` contains additional information about the wordlist. The wordlist is used as the project's dictionary input for academic coursework; this repository does not independently certify its provenance or redistribution permissions.

---

## Academic Information

**Project:** Scrabble.pluto  
**Course:** CSD311 – Artificial Intelligence  
**Institution:** SNIoE
**Project Team:** Pranshu Upadhyay, Sanya Tripathi, Rhytima Madan, Riya Arora, Sabarigirish Manikandan, Aarush Chandra, Ayan Pandey
**Faculty:** Snehasis Mukherjee

---

## Acknowledgements

Developed as part of the CSD311 Artificial Intelligence course project.

**Scrabble.pluto — A Trie-powered, heuristic-driven approach to intelligent Scrabble gameplay.**
