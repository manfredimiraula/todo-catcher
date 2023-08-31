import os
from src.utils.logging import Logger
from src.todo_catcher.catcher import ToDoCatcher


def read_file_extension(file: str) -> str:
    """Read the file path and provide the file name and the extension
        of that file.

    Parameters
    ----------
        file : str
            The path to the file.

    Returns
    -------
        file_name, extension : str, str
            The file name and the extension of the file.
    """

    file_name, extension = os.path.splitext(file)

    return file_name, extension


def scan_directory(logger: Logger, directory: str = None, exclude: list = None):
    """Scan a directory, or if not provided, the root folder
        to look for .py file and catch TODOs. Leverages the class
        ToDoCatcher

    Parameters
    ----------
        directory : str
            The directory path. (Default=None)

    Returns
    -------
        all_todos : list(dict)
            Return the fill list of TODOs found
    """

    if directory is None:
        directory = os.getcwd()  # get current working directory

    all_todos = []

    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith(".py"):
                filepath = os.path.join(root, file)
                catcher = ToDoCatcher(logger, filepath)
                todos = catcher._catch_todos()
                if len(todos) > 0:
                    all_todos.append(todos)

    return all_todos
