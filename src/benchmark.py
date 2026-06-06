import csv
import os


class Benchmark:

    @staticmethod
    def save(
        filename,
        original_size,
        compressed_size,
        execution_time
    ):

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

        benchmark_file = (
            "outputs/benchmark.csv"
        )

        file_exists = os.path.exists(
            benchmark_file
        )

        with open(
            benchmark_file,
            "a",
            newline="",
            encoding="utf-8"
        ) as file:

            writer = csv.writer(
                file
            )

            if not file_exists:

                writer.writerow(
                    [
                        "File",
                        "Original Size",
                        "Compressed Size",
                        "Compression Ratio",
                        "Execution Time"
                    ]
                )

            writer.writerow(
                [
                    filename,
                    original_size,
                    compressed_size,
                    ratio,
                    execution_time
                ]
            )