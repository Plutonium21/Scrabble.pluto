from .board import is_board_empty, is_inside_board, get_neighbours
from .scoring import score_placement

DIRECTIONS = {"H": (0,1), "V": (1,0)}

def validate_move(board, rack, word, row, col, orientation, dictionary):
    word = word.strip().upper()
    if orientation not in DIRECTIONS:
        return False, "Choose horizontal or vertical.", None
    if len(word) < 2 or word not in dictionary:
        return False, f"{word or 'That word'} is not in the loaded lexicon.", None
    if not is_inside_board(row,col):
        return False, "Starting square is outside the board.", None
    dr,dc = DIRECTIONS[orientation]

    # A submitted word must begin at the actual beginning of its main run.
    before = (row-dr,col-dc)
    if is_inside_board(*before) and board[before[0]][before[1]] is not None:
        return False, "Your word starts too late. Include the existing letter before it.", None

    available = [t.letter if not t.is_blank else "?" for t in rack]
    placements = {}
    used_indices = []
    for i,letter in enumerate(word):
        r,c = row+i*dr,col+i*dc
        if not is_inside_board(r,c):
            return False, "The word extends beyond the board.", None
        existing = board[r][c]
        if existing is not None:
            if existing.letter != letter:
                return False, f"Square {r+1},{c+1} already contains {existing.letter}.", None
            continue

        try:
            idx = available.index(letter)
            tile = rack[idx]
        except ValueError:
            try:
                idx = available.index("?")
                tile = rack[idx].assigned(letter)
            except ValueError:
                return False, f"You need a {letter} tile (or a blank).", None
        available[idx] = None
        used_indices.append(idx)
        placements[(r,c)] = tile

    if not placements:
        return False, "A move must place at least one new tile.", None

    after = (row+len(word)*dr,col+len(word)*dc)
    if is_inside_board(*after) and board[after[0]][after[1]] is not None:
        return False, "Your word ends too early; include the existing letter after it.", None

    if is_board_empty(board):
        if (7,7) not in placements:
            return False, "Your opening move must cover the centre square.", None
    else:
        connected = any(
            board[nr][nc] is not None
            for r,c in placements
            for nr,nc in get_neighbours(r,c)
        )
        if not connected:
            return False, "Your move must connect to a tile already on the board.", None

    # Validate all perpendicular words. For H, inspect vertical; for V, horizontal.
    cr,cc = dc,dr
    for (r,c),tile in placements.items():
        letters = []
        rr,ccur = r-cr,c-cc
        while is_inside_board(rr,ccur) and board[rr][ccur] is not None:
            letters.insert(0,board[rr][ccur].letter)
            rr -= cr; ccur -= cc
        letters.append(tile.letter)
        rr,ccur = r+cr,c+cc
        while is_inside_board(rr,ccur) and board[rr][ccur] is not None:
            letters.append(board[rr][ccur].letter)
            rr += cr; ccur += cc
        if len(letters)>1 and "".join(letters) not in dictionary:
            return False, f"Invalid cross-word: {''.join(letters)}.", None

    score = score_placement(board,placements,(dr,dc),len(used_indices))
    return True,"Legal move.",{
        "word":word,"placements":placements,"used_indices":used_indices,
        "score":score,"row":row,"col":col,"orientation":orientation
    }

def apply_move(board,rack,move):
    for (r,c),tile in move["placements"].items():
        board[r][c] = tile
    for index in sorted(move["used_indices"],reverse=True):
        rack.pop(index)
