from .constants import BOARD_SIZE

# Standard Scrabble premium layout, zero-based row/column coordinates.
TRIPLE_WORD = {
    (0,0),(0,7),(0,14),(7,0),(7,14),(14,0),(14,7),(14,14)
}
DOUBLE_WORD = {
    (1,1),(2,2),(3,3),(4,4),(7,7),(10,10),(11,11),(12,12),(13,13),
    (1,13),(2,12),(3,11),(4,10),(10,4),(11,3),(12,2),(13,1)
}
TRIPLE_LETTER = {
    (1,5),(1,9),(5,1),(5,5),(5,9),(5,13),
    (9,1),(9,5),(9,9),(9,13),(13,5),(13,9)
}
DOUBLE_LETTER = {
    (0,3),(0,11),(2,6),(2,8),(3,0),(3,7),(3,14),
    (6,2),(6,6),(6,8),(6,12),(7,3),(7,11),
    (8,2),(8,6),(8,8),(8,12),(11,0),(11,7),(11,14),
    (12,6),(12,8),(14,3),(14,11)
}

def create_empty_board():
    return [[None for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]

def is_inside_board(row, col):
    return 0 <= row < BOARD_SIZE and 0 <= col < BOARD_SIZE

def is_board_empty(board):
    return all(tile is None for row in board for tile in row)

def get_neighbours(row, col):
    candidates = ((row-1,col),(row+1,col),(row,col-1),(row,col+1))
    return [(r,c) for r,c in candidates if is_inside_board(r,c)]

def premium_at(row, col):
    if (row,col) in TRIPLE_WORD: return "TW"
    if (row,col) in DOUBLE_WORD: return "DW"
    if (row,col) in TRIPLE_LETTER: return "TL"
    if (row,col) in DOUBLE_LETTER: return "DL"
    return ""

def place_tile(board, row, col, tile):
    if not is_inside_board(row,col):
        raise ValueError("Position is outside the board.")
    if board[row][col] is not None:
        raise ValueError("Square is already occupied.")
    board[row][col] = tile
