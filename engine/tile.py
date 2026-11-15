from dataclasses import dataclass
from .constants import LETTER_VALUES

@dataclass(frozen=True)
class Tile:
    letter: str
    value: int
    is_blank: bool = False

    @classmethod
    def from_letter(cls, letter):
        letter = letter.upper()
        if letter == "?":
            return cls("?", 0, True)
        if letter not in LETTER_VALUES:
            raise ValueError(f"Invalid tile: {letter}")
        return cls(letter, LETTER_VALUES[letter], False)

    def assigned(self, letter):
        """A blank keeps zero points after being assigned a visible letter."""
        if not self.is_blank:
            return self
        letter = letter.upper()
        if letter not in LETTER_VALUES:
            raise ValueError(f"Invalid blank assignment: {letter}")
        return Tile(letter, 0, True)
