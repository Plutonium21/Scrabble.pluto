from engine.board import create_empty_board
from engine.tile import Tile
from engine.scoring import score_placement

def test_blank_zero_value():
    b=create_empty_board()
    p={(7,7):Tile("A",0,True),(7,8):Tile.from_letter("T")}
    assert score_placement(b,p,(0,1),2)==2
