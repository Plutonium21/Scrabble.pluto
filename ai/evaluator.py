def evaluate_move(move):
    # Immediate points dominate; modestly reward using more rack tiles.
    return move["score"] + 0.20*len(move["used_indices"])

def choose_move(board,rack,dictionary,trie):
    from .move_generator import TrieMoveGenerator
    generator = TrieMoveGenerator(trie,dictionary)
    # The generator stores start coordinates per search branch.
    moves = generator.generate(board,rack)
    return max(moves,key=evaluate_move,default=None)
