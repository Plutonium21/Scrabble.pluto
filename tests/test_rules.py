from engine.board import create_empty_board
from engine.tile import Tile
from engine.dictionary import Dictionary
from engine.rules import validate_move,apply_move

def test_opening_move_covers_center():
    b=create_empty_board(); rack=[Tile.from_letter(x) for x in "CAT"]
    assert validate_move(b,rack,"CAT",7,6,"H",Dictionary(["CAT"]))[0]
    assert not validate_move(b,rack,"CAT",0,0,"H",Dictionary(["CAT"]))[0]

def test_move_uses_rack_tiles():
    b=create_empty_board(); rack=[Tile.from_letter(x) for x in "CAT"]
    ok,_,m=validate_move(b,rack,"CAT",7,6,"H",Dictionary(["CAT"]))
    assert ok
    apply_move(b,rack,m)
    assert len(rack)==0 and b[7][6].letter=="C"
