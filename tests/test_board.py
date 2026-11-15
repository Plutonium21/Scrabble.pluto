from engine.board import *
from engine.tile import Tile

def test_board_shape():
    b=create_empty_board()
    assert len(b)==15 and all(len(row)==15 for row in b)

def test_premium_counts():
    assert (len(TRIPLE_WORD),len(DOUBLE_WORD),len(TRIPLE_LETTER),len(DOUBLE_LETTER))==(8,17,12,24)

def test_centre_double_word():
    assert premium_at(7,7)=="DW"

def test_neighbours_corner():
    assert len(get_neighbours(0,0))==2

def test_blank_assignment_stays_zero():
    assert Tile.from_letter("?").assigned("A").value==0
