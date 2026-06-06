import argparse
import logging
import os
import time

from src.huffman import HuffmanCoding
from src.compressor import Compressor
from src.decompressor import Decompressor
from src.archive_manager import ArchiveManager
from src.analytics import Analytics
from src.benchmark import Benchmark
from src.database import CompressionDatabase
from src.utils import file_hash


# ==================================================
# Logging Configuration
# ==================================================

logging.basicConfig(
    filename="logs/app.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)


# ==================================================
# Single File Compression
# ==================================================

def compress_file(file_path):

    huffman = HuffmanCoding()

    with open(
        file_path,
        "r",
        encoding="utf-8"
    ) as file:

        text = file.read()

    frequency = huffman.build_frequency_table(
        text
    )

    huffman.build_heap(
        frequency
    )

    root = huffman.build_tree()

    huffman.generate_codes(
        root
    )

    # -----------------------------------------
    # Benchmark Timer Start
    # -----------------------------------------

    start_time = time.time()

    original_size, compressed_size = (
        Compressor.compress(
            file_path,
            "compressed_files/compressed.bin",
            huffman
        )
    )

    end_time = time.time()

    execution_time = round(
        end_time - start_time,
        6
    )

    # -----------------------------------------
    # Compression Ratio
    # -----------------------------------------

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

    # -----------------------------------------
    # Analytics
    # -----------------------------------------

    Analytics.generate(
        original_size,
        compressed_size
    )

    # -----------------------------------------
    # Benchmark
    # -----------------------------------------

    Benchmark.save(
        os.path.basename(
            file_path
        ),
        original_size,
        compressed_size,
        execution_time
    )
    CompressionDatabase.save_record(
    os.path.basename(
        file_path
    ),
    original_size,
    compressed_size,
    ratio,
    execution_time
)

    # -----------------------------------------
    # Output
    # -----------------------------------------

    print("\nCompression Completed")
    print("-" * 40)

    print(
        f"Original Size : {original_size} bytes"
    )

    print(
        f"Compressed Size : {compressed_size} bytes"
    )

    print(
        f"Compression Ratio : {ratio}%"
    )

    print(
        f"Execution Time : {execution_time} sec"
    )

    # -----------------------------------------
    # Save Report
    # -----------------------------------------

    with open(
        "outputs/compression_report.txt",
        "w",
        encoding="utf-8"
    ) as report:

        report.write(
            "Compression Report\n"
        )

        report.write(
            "=" * 30 + "\n"
        )

        report.write(
            f"Original Size : {original_size} bytes\n"
        )

        report.write(
            f"Compressed Size : {compressed_size} bytes\n"
        )

        report.write(
            f"Compression Ratio : {ratio}%\n"
        )

        report.write(
            f"Execution Time : {execution_time} sec\n"
        )

    logging.info(
        f"Compression Completed | Ratio={ratio}% | Time={execution_time}"
    )


# ==================================================
# Single File Decompression
# ==================================================

def decompress_file():

    Decompressor.decompress(
        "compressed_files/compressed.bin",
        "decompressed_files/restored.txt"
    )

    print(
        "\nDecompression Completed"
    )

    logging.info(
        "Single File Decompression Completed"
    )

    verify_files()


# ==================================================
# File Verification
# ==================================================

def verify_files():

    global LAST_COMPRESSED_FILE

    original_file = LAST_COMPRESSED_FILE

    restored_file = (
        "decompressed_files/restored.txt"
    )

    if not os.path.exists(
        restored_file
    ):

        print(
            "\nVerification Failed"
        )

        print(
            "Restored file not found"
        )

        return

    original_hash = file_hash(
        original_file
    )

    restored_hash = file_hash(
        restored_file
    )

    print("\nVerification")
    print("-" * 40)

    if original_hash == restored_hash:

        print(
            "Files Match Successfully"
        )

        logging.info(
            "Integrity Verification Passed"
        )

    else:

        print(
            "Verification Failed"
        )

        logging.error(
            "Integrity Verification Failed"
        )


# ==================================================
# Folder Compression (V6)
# ==================================================

def compress_folder(folder):

    os.makedirs(
        "archives",
        exist_ok=True
    )

    count = ArchiveManager.create_archive(
        folder,
        "archives/archive.dfc"
    )

    print(
        f"\n{count} files archived successfully"
    )

    logging.info(
        f"{count} files archived"
    )


# ==================================================
# Archive Extraction (V6)
# ==================================================

def extract_archive(
    archive_path
):

    count = (
        ArchiveManager.extract_archive(
            archive_path,
            "decompressed_files"
        )
    )

    print(
        f"\n{count} files extracted successfully"
    )

    logging.info(
        f"{count} files extracted"
    )


# ==================================================
# Analyze Report
# ==================================================

def analyze_report():

    report_path = (
        "outputs/compression_report.txt"
    )

    if os.path.exists(
        report_path
    ):

        print(
            "\nCompression Report"
        )

        print("=" * 40)

        with open(
            report_path,
            "r",
            encoding="utf-8"
        ) as report:

            print(
                report.read()
            )

    else:

        print(
            "No compression report found."
        )


# ==================================================
# Benchmark Report
# ==================================================

def show_benchmark():

    file_path = (
        "outputs/benchmark.csv"
    )

    if os.path.exists(
        file_path
    ):

        print(
            "\nBenchmark Report"
        )

        print("=" * 40)

        with open(
            file_path,
            "r",
            encoding="utf-8"
        ) as file:

            print(
                file.read()
            )

    else:

        print(
            "No benchmark data found."
        )

# ==================================================
# Database Initialization
# ==================================================

CompressionDatabase.initialize()

# ==================================================
# CLI Configuration
# ==================================================

parser = argparse.ArgumentParser(
    description=
    "Dynamic File Compression Utility Pro"
)

subparsers = parser.add_subparsers(
    dest="command"
)


# --------------------------------------------------
# Compress
# --------------------------------------------------

compress_parser = (
    subparsers.add_parser(
        "compress",
        help="Compress a file"
    )
)

compress_parser.add_argument(
    "file",
    help="Input text file"
)


# --------------------------------------------------
# Decompress
# --------------------------------------------------

subparsers.add_parser(
    "decompress",
    help="Decompress compressed.bin"
)


# --------------------------------------------------
# Analyze
# --------------------------------------------------

subparsers.add_parser(
    "analyze",
    help="Show compression report"
)


# --------------------------------------------------
# Benchmark
# --------------------------------------------------

subparsers.add_parser(
    "benchmark",
    help="Show benchmark history"
)


# --------------------------------------------------
# Folder Compression (V6)
# --------------------------------------------------

folder_parser = (
    subparsers.add_parser(
        "compress-folder",
        help="Compress entire folder"
    )
)

folder_parser.add_argument(
    "folder",
    help="Folder path"
)


# --------------------------------------------------
# Extract Archive (V6)
# --------------------------------------------------

extract_parser = (
    subparsers.add_parser(
        "extract",
        help="Extract archive"
    )
)

extract_parser.add_argument(
    "archive",
    help="Archive path"
)


args = parser.parse_args()


# ==================================================
# Command Routing
# ==================================================

if args.command == "compress":

    compress_file(args.file
    )

elif args.command == "decompress":

    decompress_file()

elif args.command == "compress-folder":

    compress_folder(
        args.folder
    )

elif args.command == "extract":

    extract_archive(
        args.archive
    )

elif args.command == "analyze":

    analyze_report()

elif args.command == "benchmark":

    show_benchmark()

else:

    parser.print_help()