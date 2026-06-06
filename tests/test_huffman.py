from src.huffman import HuffmanCoding


def test_frequency():

    h = HuffmanCoding()

    freq = h.build_frequency_table("aaabb")

    assert freq["a"] == 3
    assert freq["b"] == 2


def test_encode_decode():

    h = HuffmanCoding()

    text = "hello"

    freq = h.build_frequency_table(text)

    h.build_heap(freq)

    root = h.build_tree()

    h.generate_codes(root)

    encoded = h.encode_text(text)

    decoded = h.decode_text(encoded)

    assert decoded == text