import random
from .constants import TILE_DISTRIBUTION, RACK_SIZE
from .tile import Tile

class TileBag:
    def __init__(self, seed=None):
        self.rng = random.Random(seed)
        self.tiles = [
            Tile.from_letter(letter)
            for letter, count in TILE_DISTRIBUTION.items()
            for _ in range(count)
        ]
        self.rng.shuffle(self.tiles)

    def draw(self, count):
        count = min(max(0, count), len(self.tiles))
        result = self.tiles[:count]
        del self.tiles[:count]
        return result

    def exchange(self, rack, indices):
        if len(self.tiles) < RACK_SIZE:
            raise ValueError("At least 7 tiles must remain in the bag to exchange.")
        indices = sorted(set(indices))
        if any(i < 0 or i >= len(rack) for i in indices):
            raise ValueError("Invalid rack index.")
        replacements = self.draw(len(indices))
        returned = [rack[i] for i in indices]
        for i, tile in zip(indices, replacements):
            rack[i] = tile
        self.tiles.extend(returned)
        self.rng.shuffle(self.tiles)
        return rack

def initial_rack(bag):
    return bag.draw(RACK_SIZE)
