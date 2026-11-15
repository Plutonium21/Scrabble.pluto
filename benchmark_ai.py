
import time
import statistics

from engine.dictionary import load_dictionary
from engine.board import create_empty_board
from engine.tile import Tile
from engine.tile_bag import TileBag
from engine.rules import validate_move, apply_move
from ai.trie import Trie
from ai.move_generator import TrieMoveGenerator


def benchmark_generator(generator, board, rack, runs=3):
    """Measure move-generation time over multiple runs."""

    timings = []
    moves = []

    for _ in range(runs):
        start = time.perf_counter()
        moves = list(generator.generate(board, rack))
        elapsed = time.perf_counter() - start
        timings.append(elapsed)

    return {
        "moves": moves,
        "average": statistics.mean(timings),
        "median": statistics.median(timings),
        "fastest": min(timings)
    }


def main():
    print("=" * 55)
    print("SCRABBLE AI - MOVE GENERATION BENCHMARK")
    print("=" * 55)

    # 1. Load the full dictionary.
    start = time.perf_counter()
    dictionary, source = load_dictionary()
    dictionary_time = time.perf_counter() - start

    print(f"\nDictionary source: {source}")
    print(f"Words loaded: {len(dictionary):,}")
    print(f"Dictionary loading: {dictionary_time:.3f} seconds")

    # 2. Construct the Trie.
    start = time.perf_counter()
    trie = Trie(dictionary)
    trie_time = time.perf_counter() - start

    print(f"Trie words: {trie.word_count:,}")
    print(f"Trie construction: {trie_time:.3f} seconds")

    generator = TrieMoveGenerator(trie, dictionary)

    # 3. Opening board benchmark.
    opening_board = create_empty_board()
    opening_rack = TileBag(seed=42).draw(7)

    print("\n--- OPENING BOARD ---")
    print("Rack:", " ".join(t.letter for t in opening_rack))

    opening_result = benchmark_generator(
        generator, opening_board, opening_rack
    )

    print(f"Legal moves generated: {len(opening_result['moves']):,}")
    print(f"Average time: {opening_result['average']:.4f} seconds")
    print(f"Median time: {opening_result['median']:.4f} seconds")
    print(f"Fastest time: {opening_result['fastest']:.4f} seconds")

    # 4. Create a board with one legal opening word.
    board = create_empty_board()
    rack = [Tile.from_letter(x) for x in "CAT"]

    ok, message, move = validate_move(
        board, rack, "CAT", 7, 6, "H", dictionary
    )

    if not ok:
        print("\nCould not create benchmark board:", message)
        return

    apply_move(board, rack, move)

    # 5. Add a legal extension to create an early-game position.
    extension_rack = [Tile.from_letter("S")]

    ok, message, move = validate_move(
        board, extension_rack, "CATS", 7, 6, "H", dictionary
    )

    if ok:
        apply_move(board, extension_rack, move)
    else:
        print("\nNote: CATS extension unavailable:", message)

    # Use a fresh rack for the AI search.
    test_rack = TileBag(seed=123).draw(7)

    print("\n--- EARLY-GAME BOARD ---")
    print("Existing word: CATS" if ok else "Existing word: CAT")
    print("Rack:", " ".join(t.letter for t in test_rack))

    early_result = benchmark_generator(
        generator, board, test_rack
    )

    print(f"Legal moves generated: {len(early_result['moves']):,}")
    print(f"Average time: {early_result['average']:.4f} seconds")
    print(f"Median time: {early_result['median']:.4f} seconds")
    print(f"Fastest time: {early_result['fastest']:.4f} seconds")

    # 6. Final summary.
    print("\n" + "=" * 55)
    print("BENCHMARK SUMMARY")
    print("=" * 55)

    print(f"Dictionary loading: {dictionary_time:.3f}s")
    print(f"Trie construction:  {trie_time:.3f}s")
    print(f"Opening search:     {opening_result['median']:.4f}s")
    print(f"Early-game search:  {early_result['median']:.4f}s")

    print("\nBenchmark completed.")


if __name__ == "__main__":
    main()
