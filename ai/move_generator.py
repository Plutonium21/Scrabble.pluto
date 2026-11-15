from engine.constants import BOARD_SIZE
from engine.rules import validate_move
from engine.board import is_inside_board, get_neighbours, is_board_empty


class TrieMoveGenerator:
    """
    Anchor-based Trie move generator.

    Instead of searching from every board square:
    - On an empty board, use the centre square as the anchor.
    - Otherwise, use empty squares adjacent to existing tiles.
    - Search only starts that can reach an anchor using the available rack.
    - Use the Trie to prune invalid prefixes immediately.
    - Pass completed candidates through validate_move().
    """

    DIRECTIONS = {
        "H": (0, 1),
        "V": (1, 0)
    }

    def __init__(self, trie, dictionary):
        self.trie = trie
        self.dictionary = dictionary

    def _get_anchors(self, board):
        """Return empty squares where a new move can connect."""
        if is_board_empty(board):
            return {(7, 7)}

        anchors = set()

        for row in range(BOARD_SIZE):
            for col in range(BOARD_SIZE):
                if board[row][col] is not None:
                    continue

                if any(
                    board[nr][nc] is not None
                    for nr, nc in get_neighbours(row, col)
                ):
                    anchors.add((row, col))

        return anchors

    def _get_start_positions(self, board, anchor, dr, dc, rack_size):
        """
        Find valid word starts that can reach this anchor.

        A start must:
        - Be on the same row/column as the anchor.
        - Have no existing tile immediately before it.
        - Require no more than rack_size new tiles to reach the anchor.
        """
        ar, ac = anchor
        starts = []

        for offset in range(BOARD_SIZE):
            row = ar - offset * dr
            col = ac - offset * dc

            if not is_inside_board(row, col):
                break

            previous = (row - dr, col - dc)

            if is_inside_board(*previous):
                pr, pc = previous
                if board[pr][pc] is not None:
                    continue

            empty_count = 0

            for step in range(offset + 1):
                rr = row + step * dr
                cc = col + step * dc

                if board[rr][cc] is None:
                    empty_count += 1

            if empty_count <= rack_size:
                starts.append((row, col))

        return starts

    def generate(self, board, rack):
        """Generate unique legal moves using anchor squares."""
        found = {}
        anchors = self._get_anchors(board)

        for orientation, (dr, dc) in self.DIRECTIONS.items():
            for anchor in anchors:
                start_positions = self._get_start_positions(
                    board, anchor, dr, dc, len(rack)
                )

                for row, col in start_positions:
                    self._walk(
                        board=board,
                        rack=rack,
                        orientation=orientation,
                        dr=dr,
                        dc=dc,
                        row=row,
                        col=col,
                        node=self.trie.root,
                        prefix="",
                        placements={},
                        used_indices=[],
                        anchor=anchor,
                        found=found,
                        start_row=row,
                        start_col=col
                    )

        yield from found.values()

    def _walk(
        self, board, rack, orientation, dr, dc,
        row, col, node, prefix, placements,
        used_indices, anchor, found, start_row, start_col
    ):
        """Recursively walk Trie branches along a board line."""

        # Reached the board boundary.
        if not is_inside_board(row, col):
            if node.is_word and len(prefix) >= 2:
                self._record_candidate(
                    board, rack, orientation, prefix,
                    placements, anchor, found, start_row, start_col
                )
            return

        existing = board[row][col]

        # An existing tile forces the corresponding Trie edge.
        if existing is not None:
            child = node.children.get(existing.letter)

            if child is not None:
                self._walk(
                    board, rack, orientation, dr, dc,
                    row + dr, col + dc,
                    child, prefix + existing.letter,
                    placements, used_indices, anchor, found,
                    start_row, start_col
                )
            return

        # Empty square: a valid word may end here.
        if node.is_word and len(prefix) >= 2:
            self._record_candidate(
                board, rack, orientation, prefix,
                placements, anchor, found, start_row, start_col
            )

        # Try available rack tiles.
        choices = {}

        for idx, tile in enumerate(rack):
            if idx in used_indices:
                continue

            letters = (
                "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
                if tile.is_blank
                else tile.letter
            )

            for letter in letters:
                child = node.children.get(letter)

                if child is not None and letter not in choices:
                    choices[letter] = (child, idx, tile)

        for letter, (child, idx, tile) in choices.items():
            placements[(row, col)] = (
                tile.assigned(letter) if tile.is_blank else tile
            )
            used_indices.append(idx)

            self._walk(
                board, rack, orientation, dr, dc,
                row + dr, col + dc,
                child, prefix + letter,
                placements, used_indices, anchor, found, start_row, start_col
            )

            used_indices.pop()
            placements.pop((row, col), None)

    def _record_candidate(
        self, board, rack, orientation, word,
        placements, anchor, found, start_row, start_col
    ):
        """Validate and store candidates that use the current anchor."""

        # A generated word must actually place a tile on this anchor.
        if anchor not in placements:
            return

        row, col = start_row, start_col

        ok, _, move = validate_move(
            board,
            rack,
            word,
            row,
            col,
            orientation,
            self.dictionary
        )

        if ok:
            key = (
                move["word"],
                move["row"],
                move["col"],
                move["orientation"]
            )
            found[key] = move



'''
Old version
The older version move generator searches every possible starting square in both directions. That is correct as a basic approach, but it does unnecessary work. With a large lexicon, a 16-second search is too slow for a comfortable game.
I'd like to improve it using anchor-square-based move generation: search around existing tiles and the centre square rather than treating every board square as a possible starting point. We can also add cross-check constraints later.
One more thing I want to preserve: blank tiles must be treated as wildcards during search, but their assigned value must remain zero when the move is scored.

class TrieMoveGenerator:
    """
    Trie-guided board search.

    For every possible beginning of a horizontal/vertical word, walk the Trie.
    Existing board cells force one edge; empty cells branch only over letters
    present in the rack. A branch dies immediately if the Trie has no matching
    child. Completed candidates are passed through the authoritative rule checker.
    """
    def __init__(self,trie,dictionary):
        self.trie = trie
        self.dictionary = dictionary

    def generate(self,board,rack):
        found = {}
        for orientation,(dr,dc) in (("H",(0,1)),("V",(1,0))):
            for row in range(BOARD_SIZE):
                for col in range(BOARD_SIZE):
                    prev = (row-dr,col-dc)
                    if 0 <= prev[0] < BOARD_SIZE and 0 <= prev[1] < BOARD_SIZE:
                        if board[prev[0]][prev[1]] is not None:
                            continue
                    self._start_row,self._start_col = row,col
                    self._walk(board,rack,orientation,dr,dc,row,col,
                               self.trie.root,"",{},[],found)
        yield from found.values()

    def _walk(self,board,rack,orientation,dr,dc,row,col,node,prefix,
              placements,used_indices,found):
        # If we stepped just beyond the edge, the preceding prefix may be a word.
        if not (0 <= row < BOARD_SIZE and 0 <= col < BOARD_SIZE):
            if node.is_word and len(prefix) >= 2:
                self._record_candidate(board,rack,orientation,prefix,found)
            return

        # A word can end immediately before an empty square. If this square
        # already contains a tile, the main word must continue through it.
        if node.is_word and len(prefix) >= 2 and board[row][col] is None:
            self._record_candidate(board,rack,orientation,prefix,found)

        existing = board[row][col]
        if existing is not None:
            child = node.children.get(existing.letter)
            if child is not None:
                self._walk(board,rack,orientation,dr,dc,row+dr,col+dc,child,
                           prefix+existing.letter,placements,used_indices,found)
            return

        # Empty square: branch over each distinct available rack letter.
        choices = {}
        for idx,tile in enumerate(rack):
            if idx in used_indices:
                continue
            letter_options = "ABCDEFGHIJKLMNOPQRSTUVWXYZ" if tile.is_blank else tile.letter
            for letter in letter_options:
                child = node.children.get(letter)
                if child is not None:
                    choices.setdefault(letter,(child,idx,tile))
        for letter,(child,idx,tile) in choices.items():
            placements[(row,col)] = tile.assigned(letter) if tile.is_blank else tile
            used_indices.append(idx)
            self._walk(board,rack,orientation,dr,dc,row+dr,col+dc,child,
                       prefix+letter,placements,used_indices,found)
            used_indices.pop()
            placements.pop((row,col),None)

    def _record_candidate(self,board,rack,orientation,word,found):
        ok,_,move = validate_move(
            board,rack,word,self._start_row,self._start_col,
            orientation,self.dictionary
        )
        if ok:
            key = (move["word"],move["row"],move["col"],orientation)
            found[key] = move

    def _set_start(self,row,col):
        self._start_row,self._start_col = row,col
'''