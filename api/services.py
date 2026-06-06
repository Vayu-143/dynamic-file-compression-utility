import os
import tempfile

from src.huffman import HuffmanCoding
from src.compressor import Compressor
from src.decompressor import Decompressor


# ==================================================
# Compression Service
# ==================================================

class CompressionService:

    @staticmethod
    def compress_uploaded_file(content):

        temp_input = tempfile.NamedTemporaryFile(
            delete=False,
            suffix=".txt"
        )

        temp_input.write(content)
        temp_input.close()

        huffman = HuffmanCoding()

        with open(
            temp_input.name,
            "r",
            encoding="utf-8"
        ) as file:

            text = file.read()

        frequency = (
            huffman.build_frequency_table(
                text
            )
        )

        huffman.build_heap(
            frequency
        )

        root = huffman.build_tree()

        huffman.generate_codes(
            root
        )

        output_file = (
            "compressed_files/api_compressed.bin"
        )

        original_size, compressed_size = (
            Compressor.compress(
                temp_input.name,
                output_file,
                huffman
            )
        )

        os.remove(
            temp_input.name
        )

        ratio = round(
            (
                (
                    original_size -
                    compressed_size
                )
                / original_size
            ) * 100,
            2
        )

        return {
            "original_size":
                original_size,

            "compressed_size":
                compressed_size,

            "compression_ratio":
                ratio
        }


# ==================================================
# Decompression Service
# ==================================================

class DecompressionService:

    @staticmethod
    def decompress_uploaded_file(
        binary_content,
        metadata_content
    ):

        temp_bin = tempfile.NamedTemporaryFile(
            delete=False,
            suffix=".bin"
        )

        temp_bin.write(
            binary_content
        )

        temp_bin.close()

        metadata_path = (
            temp_bin.name + ".json"
        )

        with open(
            metadata_path,
            "wb"
        ) as file:

            file.write(
                metadata_content
            )

        output_file = (
            "decompressed_files/api_restored.txt"
        )

        Decompressor.decompress(
            temp_bin.name,
            output_file
        )

        with open(
            output_file,
            "r",
            encoding="utf-8"
        ) as file:

            restored_text = (
                file.read()
            )

        os.remove(
            temp_bin.name
        )

        os.remove(
            metadata_path
        )

        return {
            "status":
                "success",

            "restored_text":
                restored_text,

            "characters":
                len(
                    restored_text
                )
        }