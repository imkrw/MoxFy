import os

"""Get the file name without the extension from a given file path."""


def get_file_name(file_path):
    basename = os.path.basename(file_path)
    return basename.split(".")[0]
