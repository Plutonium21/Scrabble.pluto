from dataclasses import dataclass, field

@dataclass
class TrieNode:
    children: dict = field(default_factory=dict)
    is_word: bool = False

class Trie:
    """Prefix tree. Each edge stores one letter; terminal nodes mark complete words."""
    def __init__(self, words=()):
        self.root = TrieNode()
        self.word_count = 0
        for word in words:
            self.insert(word)

    def insert(self, word):
        word = word.strip().upper()
        if len(word) < 2 or not word.isalpha():
            return
        node = self.root
        for letter in word:
            node = node.children.setdefault(letter, TrieNode())
        if not node.is_word:
            node.is_word = True
            self.word_count += 1

    def search(self, word):
        node = self._walk(word)
        return bool(node and node.is_word)

    def starts_with(self, prefix):
        return self._walk(prefix) is not None

    def _walk(self, text):
        node = self.root
        for letter in text.upper():
            node = node.children.get(letter)
            if node is None:
                return None
        return node
