from engine.board import create_empty_board
from engine.tile import Tile
from engine.dictionary import Dictionary
from ai.trie import Trie
from ai.evaluator import choose_move
from ai.move_generator import TrieMoveGenerator

def test_trie_ai_finds_opening():
    d=Dictionary(["CAT","ACT"])
    t=Trie(d)
    rack=[Tile.from_letter(x) for x in "CAT"]
    move=choose_move(create_empty_board(),rack,d,t)
    assert move is not None and move["score"]>0

def test_trie_ai_uses_existing_board_letter():
    board=create_empty_board()
    board[7][7]=Tile.from_letter("A")
    d=Dictionary(["CAT"])
    trie=Trie(d)
    rack=[Tile.from_letter("C"),Tile.from_letter("T")]
    move=choose_move(board,rack,d,trie)
    assert move is not None


def get_generated_moves(board, rack, words):
    """Build a small Trie and return all generated legal moves."""
    dictionary = Dictionary(words)
    trie = Trie(dictionary)

    generator = TrieMoveGenerator(trie, dictionary)
    return list(generator.generate(board, rack))


def test_generator_finds_horizontal_connection():
    board = create_empty_board()
    board[7][7] = Tile.from_letter("A")

    rack = [Tile.from_letter("C"), Tile.from_letter("T")]

    moves = get_generated_moves(board, rack, ["CAT"])

    assert any(
        move["word"] == "CAT"
        and move["orientation"] == "H"
        and move["row"] == 7
        and move["col"] == 6
        for move in moves
    )


def test_generator_finds_vertical_connection():
    board = create_empty_board()
    board[7][7] = Tile.from_letter("A")

    rack = [Tile.from_letter("C"), Tile.from_letter("T")]

    moves = get_generated_moves(board, rack, ["CAT"])

    assert any(
        move["word"] == "CAT"
        and move["orientation"] == "V"
        and move["row"] == 6
        and move["col"] == 7
        for move in moves
    )


def test_generator_extends_existing_word():
    board = create_empty_board()
    board[7][7] = Tile.from_letter("A")
    board[7][8] = Tile.from_letter("T")

    rack = [Tile.from_letter("C"), Tile.from_letter("S")]

    moves = get_generated_moves(board, rack, ["CATS"])

    assert any(
        move["word"] == "CATS"
        and move["orientation"] == "H"
        and move["row"] == 7
        and move["col"] == 6
        for move in moves
    )


def test_generator_validates_perpendicular_words():
    board = create_empty_board()

    # Existing A forms the main word CAT.
    board[7][7] = Tile.from_letter("A")

    # Existing E makes the perpendicular word EC.
    board[6][6] = Tile.from_letter("E")

    rack = [Tile.from_letter("C"), Tile.from_letter("T")]

    moves = get_generated_moves(board, rack, ["CAT", "EC"])

    assert any(
        move["word"] == "CAT"
        and move["orientation"] == "H"
        and move["row"] == 7
        and move["col"] == 6
        for move in moves
    )


def test_generator_uses_blank_tile():
    board = create_empty_board()
    board[7][7] = Tile.from_letter("A")

    rack = [
        Tile.from_letter("C"),
        Tile.from_letter("?")
    ]

    moves = get_generated_moves(board, rack, ["CAT"])

    blank_moves = [
        move for move in moves
        if move["word"] == "CAT"
        and any(tile.is_blank for tile in move["placements"].values())
    ]

    assert blank_moves

    blank_tile = next(
        tile
        for tile in blank_moves[0]["placements"].values()
        if tile.is_blank
    )

    assert blank_tile.value == 0
    assert blank_tile.letter == "T"


def test_generator_does_not_return_duplicate_moves():
    board = create_empty_board()
    board[7][7] = Tile.from_letter("A")

    rack = [Tile.from_letter("C"), Tile.from_letter("T")]

    moves = get_generated_moves(board, rack, ["CAT"])

    keys = [
        (
            move["word"],
            move["row"],
            move["col"],
            move["orientation"]
        )
        for move in moves
    ]

    assert len(keys) == len(set(keys))


def test_generator_respects_rack_constraints():
    board = create_empty_board()
    board[7][7] = Tile.from_letter("A")

    # C alone cannot complete CAT.
    rack = [Tile.from_letter("C")]

    moves = get_generated_moves(board, rack, ["CAT"])

    assert not any(move["word"] == "CAT" for move in moves)
