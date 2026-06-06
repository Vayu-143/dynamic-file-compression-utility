import json


class Decompressor:

    @staticmethod
    def remove_padding(bit_string):

        padding = int(bit_string[:8], 2)

        bit_string = bit_string[8:]

        return bit_string[:-padding]

    @staticmethod
    def decompress(bin_file, output_file):

        metadata = bin_file + ".json"

        with open(metadata, "r") as meta:
            codes = json.load(meta)

        reverse_codes = {v: k for k, v in codes.items()}

        bit_string = ""

        with open(bin_file, "rb") as file:

            byte = file.read(1)

            while byte:

                bits = bin(ord(byte))[2:].rjust(8, "0")

                bit_string += bits

                byte = file.read(1)

        encoded_text = Decompressor.remove_padding(bit_string)

        current = ""
        decoded = ""

        for bit in encoded_text:

            current += bit

            if current in reverse_codes:

                decoded += reverse_codes[current]
                current = ""

        with open(output_file, "w", encoding="utf-8") as file:
            file.write(decoded)