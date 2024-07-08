import os


def get_lib_path() -> str:
    """
    Returns the base directory path of the library.

    Returns:
        The base directory path of the library.

    """
    file_path = os.path.realpath(__file__)
    spl = file_path.split("/")
    base_dir = "/".join(spl[:-2])
    return base_dir


def get_py_path() -> str:
    """
    Returns the path to the 'construct_design' directory.

    Returns:
        The path to the 'construct_design' directory as a string.
    """
    return get_lib_path() + "/construct_design/"


def get_test_path() -> str:
    """
    Returns the path to the test directory.

    Returns:
        The path to the test directory.

    """
    return get_lib_path() + "/test"
