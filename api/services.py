import os
import time
import tempfile

from src.huffman import HuffmanCoding
from src.compressor import Compressor
from src.decompressor import Decompressor
from src.database import CompressionDatabase


# ==================================================
# Compression Service
# ==================================================

class CompressionService:

    @staticmethod
    def compress_uploaded_file(
        content,
        filename="uploaded_file.txt"
    ):

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

        start_time = time.time()

        original_size, compressed_size = (
            Compressor.compress(
                temp_input.name,
                output_file,
                huffman
            )
        )

        execution_time = round(
            time.time() - start_time,
            6
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

        print("BEFORE DATABASE INSERT")

        CompressionDatabase.save_record(
            operation="Compression",
            filename=filename,
            original_size=original_size,
            compressed_size=compressed_size,
            ratio=ratio,
            execution_time=execution_time
        )

        print("AFTER DATABASE INSERT")

        return {

            "status":
                "success",

            "filename":
                filename,

            "original_size":
                original_size,

            "compressed_size":
                compressed_size,

            "compression_ratio":
                ratio,

            "execution_time":
                execution_time
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

        CompressionDatabase.save_record(
            operation="Decompression",
            filename="restored.txt",
            original_size=len(binary_content),
            compressed_size=len(restored_text),
            ratio=0,
            execution_time=0
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