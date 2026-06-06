import json


class Analytics:

    @staticmethod
    def generate(
        original_size,
        compressed_size,
        total_files=1
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

        data = {
            "total_files": total_files,
            "original_size": original_size,
            "compressed_size": compressed_size,
            "compression_ratio": ratio
        }

        with open(
            "outputs/analytics.json",
            "w",
            encoding="utf-8"
        ) as file:

            json.dump(
                data,
                file,
                indent=4
            )

        return data