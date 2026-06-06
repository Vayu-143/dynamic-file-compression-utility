import os
import json

from src.huffman import HuffmanCoding


class ArchiveManager:

    @staticmethod
    def create_archive(folder_path, archive_path):

        archive = {
            "files": []
        }

        for file_name in os.listdir(folder_path):

            file_path = os.path.join(
                folder_path,
                file_name
            )

            if not os.path.isfile(file_path):
                continue

            with open(
                file_path,
                "r",
                encoding="utf-8"
            ) as file:

                text = file.read()

            huffman = HuffmanCoding()

            frequency = huffman.build_frequency_table(
                text
            )

            huffman.build_heap(
                frequency
            )

            root = huffman.build_tree()

            huffman.generate_codes(root)

            encoded_text = huffman.encode_text(
                text
            )

            archive["files"].append(
                {
                    "filename": file_name,
                    "codes": huffman.codes,
                    "data": encoded_text
                }
            )

        with open(
            archive_path,
            "w",
            encoding="utf-8"
        ) as archive_file:

            json.dump(
                archive,
                archive_file,
                indent=4
            )

        return len(
            archive["files"]
        )

    @staticmethod
    def extract_archive(
        archive_path,
        output_folder
    ):

        with open(
            archive_path,
            "r",
            encoding="utf-8"
        ) as file:

            archive = json.load(file)

        for item in archive["files"]:

            filename = item["filename"]

            reverse_codes = {
                v: k
                for k, v in item[
                    "codes"
                ].items()
            }

            current = ""

            decoded = ""

            for bit in item["data"]:

                current += bit

                if current in reverse_codes:

                    decoded += reverse_codes[
                        current
                    ]

                    current = ""

            output_path = os.path.join(
                output_folder,
                filename
            )

            with open(
                output_path,
                "w",
                encoding="utf-8"
            ) as output:

                output.write(decoded)

        return len(
            archive["files"]
        )