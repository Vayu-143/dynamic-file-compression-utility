from src.huffman import HuffmanCoding


def test_heap():

    h = HuffmanCoding()

    freq = {"a": 5, "b": 2}

    h.build_heap(freq)

    assert len(h.heap) == 2