from .board import premium_at
from .constants import BINGO_BONUS, BOARD_SIZE

def _score_word(board, placements, coords):
    subtotal = 0
    word_multiplier = 1
    for r,c in coords:
        tile = placements.get((r,c), board[r][c])
        value = tile.value
        if (r,c) in placements:
            premium = premium_at(r,c)
            if premium == "DL": value *= 2
            elif premium == "TL": value *= 3
            elif premium == "DW": word_multiplier *= 2
            elif premium == "TW": word_multiplier *= 3
        subtotal += value
    return subtotal * word_multiplier

def score_placement(board, placements, direction, used_tiles):
    dr,dc = direction
    # Find the beginning of the complete main word.
    first = min(placements, key=lambda p: p[0]*dr + p[1]*dc)
    r,c = first
    while 0 <= r-dr < BOARD_SIZE and 0 <= c-dc < BOARD_SIZE and board[r-dr][c-dc] is not None:
        r -= dr; c -= dc
    main_coords = []
    while 0 <= r < BOARD_SIZE and 0 <= c < BOARD_SIZE:
        if (r,c) in placements or board[r][c] is not None:
            main_coords.append((r,c))
            r += dr; c += dc
        else:
            break
    total = _score_word(board, placements, main_coords)

    # Each new tile may create one perpendicular word.
    cr,cc = dc,dr
    for pr,pc in placements:
        r,c = pr-cr, pc-cc
        while 0 <= r < BOARD_SIZE and 0 <= c < BOARD_SIZE and board[r][c] is not None:
            r -= cr; c -= cc
        r += cr; c += cc
        cross = []
        while 0 <= r < BOARD_SIZE and 0 <= c < BOARD_SIZE:
            if (r,c) in placements or board[r][c] is not None:
                cross.append((r,c))
                r += cr; c += cc
            else:
                break
        if len(cross) > 1:
            total += _score_word(board, placements, cross)
    if used_tiles == 7:
        total += BINGO_BONUS
    return total
