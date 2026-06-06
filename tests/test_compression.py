import os


def test_input_file_exists():

    assert os.path.exists(
        "input_files/sample.txt"
    )


def test_output_folder_exists():

    assert os.path.exists(
        "compressed_files"
    )