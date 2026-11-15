from .board import create_empty_board
from .tile_bag import TileBag,initial_rack
from .constants import MAX_SCORELESS_TURNS

class GameState:
    def __init__(self,seed=None):
        self.board = create_empty_board()
        self.bag = TileBag(seed)
        self.racks = {"You":initial_rack(self.bag),"AI":initial_rack(self.bag)}
        self.scores = {"You":0,"AI":0}
        self.turn = "You"
        self.scoreless_turns = 0
        self.game_over = False
        self.history = []

    def refill(self,player):
        self.racks[player].extend(self.bag.draw(7-len(self.racks[player])))

    def next_player(self,player):
        return "AI" if player=="You" else "You"

    def finish_turn(self,player,move=None):
        if move:
            self.scores[player] += move["score"]
            self.scoreless_turns = 0
            self.history.append(f"{player}: {move['word']} (+{move['score']})")
            self.refill(player)
        else:
            self.scoreless_turns += 1
            self.history.append(f"{player} passed.")
        self.turn = self.next_player(player)
        self.check_end()

    def check_end(self):
        if self.scoreless_turns >= MAX_SCORELESS_TURNS:
            self.game_over = True
        if len(self.bag.tiles)==0 and any(len(r)==0 for r in self.racks.values()):
            self.game_over = True
        if self.game_over:
            # Basic standard tile-value adjustment at game end.
            penalties = {p:sum(t.value for t in rack) for p,rack in self.racks.items()}
            for p,penalty in penalties.items():
                self.scores[p] -= penalty
            if len(self.bag.tiles)==0 and any(len(r)==0 for r in self.racks.values()):
                out = next((p for p,r in self.racks.items() if len(r)==0),None)
                if out:
                    other = "AI" if out=="You" else "You"
                    self.scores[out] += penalties[other]
