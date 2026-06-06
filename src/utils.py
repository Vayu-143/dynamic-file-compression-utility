import hashlib


def file_hash(filepath):

    with open(filepath, "rb") as file:
        return hashlib.md5(file.read()).hexdigest()