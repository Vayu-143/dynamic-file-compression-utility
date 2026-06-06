import json
import os


class Compressor:

    @staticmethod
    def pad_encoded_text(encoded_text):

        extra_padding = 8 - len(encoded_text) % 8

        for _ in range(extra_padding):
            encoded_text += "0"

        padded_info = "{0:08b}".format(extra_padding)

        encoded_text = padded_info + encoded_text

        return encoded_text

    @staticmethod
    def get_byte_array(padded_encoded_text):

        byte_array = bytearray()

        for i in range(0, len(padded_encoded_text), 8):

            byte = padded_encoded_text[i:i + 8]

            byte_array.append(int(byte, 2))

        return byte_array

    @staticmethod
    def compress(input_path, output_path, huffman):

        with open(input_path, "r", encoding="utf-8") as file:
            text = file.read()

        encoded_text = huffman.encode_text(text)

        padded = Compressor.pad_encoded_text(encoded_text)

        bytes_data = Compressor.get_byte_array(padded)

        with open(output_path, "wb") as output:
            output.write(bytes(bytes_data))

        metadata = output_path + ".json"

        with open(metadata, "w") as meta:
            json.dump(huffman.codes, meta)

        return (
            os.path.getsize(input_path),
            os.path.getsize(output_path)
        )