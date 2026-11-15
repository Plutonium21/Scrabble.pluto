from ai.trie import Trie

def test_trie_exact_search_and_prefix():
    trie=Trie(["CAT","CAR","CARE","DOG"])
    assert trie.search("CAT")
    assert trie.search("CARE")
    assert not trie.search("CA")
    assert trie.starts_with("CA")
    assert not trie.starts_with("CZ")

def test_trie_deduplicates():
    trie=Trie(["CAT","CAT"])
    assert trie.word_count==1
