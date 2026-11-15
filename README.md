# Scrabble Club — Trie-powered Python Scrabble

## Setup (Windows PowerShell)
```powershell
py -3.12 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
python -m pytest -v
streamlit run app.py
```

## Collins 2019 word list
Place your permitted text list at `data/words.txt`. One word per line is best.
The app automatically loads `data/words.txt`, or another `.txt` file in `data/`.
The list is not included in this ZIP. Respect the licence attached to your copy.
Set a custom path with `$env:SCRABBLE_WORDLIST="D:\path\to\list.txt"`.

## AI algorithm
The AI builds a Trie from the lexicon. For each possible word start and both
orientations, it traverses the Trie across the board:
- Occupied squares force the matching letter edge.
- Empty squares branch only over letters available in the rack (or A-Z for a blank).
- A branch is pruned immediately if the Trie has no matching child.
- Completed candidate words are checked by the same move validator as human moves.
- The greedy evaluator chooses the legal move with the highest immediate score,
  with a small rack-use tie-break.

This is a Trie-guided prefix-pruned generator, not a GADDAG. It is a substantial
improvement over scanning every dictionary word at every board coordinate.
For very large lexicons, anchor-square generation and cross-check masks can
improve performance further.

## UI
Click a board square -> popup dialog -> enter the complete word -> choose
horizontal/vertical -> check move -> play word.

## Limitations to disclose
This is an educational prototype, not a tournament-certified engine.
The word list format should be checked for headers/definitions. Game challenges,
full exchange UI, and some official endgame edge cases are not implemented.
