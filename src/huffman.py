import heapq
from collections import Counter


class Node:
    def __init__(self, char, freq):
        self.char = char
        self.freq = freq
        self.left = None
        self.right = None

    def __lt__(self, other):
        return self.freq < other.freq


class HuffmanCoding:

    def __init__(self):

        self.heap = []
        self.codes = {}
        self.reverse_codes = {}

    def build_frequency_table(self, text):
        return Counter(text)

    def build_heap(self, frequency):

        for char, freq in frequency.items():
            heapq.heappush(self.heap, Node(char, freq))

    def build_tree(self):

        while len(self.heap) > 1:

            left = heapq.heappop(self.heap)
            right = heapq.heappop(self.heap)

            merged = Node(None, left.freq + right.freq)

            merged.left = left
            merged.right = right

            heapq.heappush(self.heap, merged)

        return heapq.heappop(self.heap)

    def generate_codes(self, node, current_code=""):

        if node is None:
            return

        if node.char is not None:

            self.codes[node.char] = current_code
            self.reverse_codes[current_code] = node.char

            return

        self.generate_codes(node.left, current_code + "0")
        self.generate_codes(node.right, current_code + "1")

    def encode_text(self, text):

        encoded_text = ""

        for char in text:
            encoded_text += self.codes[char]

        return encoded_text

    def decode_text(self, encoded_text):

        current_code = ""
        decoded_text = ""

        for bit in encoded_text:

            current_code += bit

            if current_code in self.reverse_codes:

                decoded_text += self.reverse_codes[current_code]
                current_code = ""

        return decoded_text