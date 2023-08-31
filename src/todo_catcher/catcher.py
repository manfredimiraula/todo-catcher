import os
import re
from src.utils.logging import Logger


class ToDoCatcher:
    """This class contains the main methods to catch TODOs.
    It assumes that the developer writes TODOs as close as possible to the code.
    It assumes that the developer store TODOs as comment with the minimum format
    # TODO ...

    Methods
    -------
    _check_py_file : staticmethod
        Check if the file is a .py file

    _catch_todos
        Scan a .py file and collects all the TODOs.
        It stores the line in which the TODO is found and
        the function or class it belongs (if the TODO is found
        within a function or class)
    """

    def __init__(
        self,
        logger: Logger,
        file: str,
    ):
        """init

        Parameters
        ----------
        file : str
            the file path containing the code we want to scan
        logger : Logger
            the logger to log events
        """
        self.file = file
        self.logger = logger

    def _catch_todos(self) -> list:
        """Scan the file passed. If a .py file,
            it stores all the TODOs, catched as comments,
            inside a list of dictionaries.
            If the comment is found within a function or a class,
            it stores the name of the function or class and the line
            where the TODO is found

        Returns
        -------
            todos : list(dict)
                A list of dictionaries with the following structure
                todo | line | function
        """
        # store todos from file
        todos = []
        # track position inside functions
        inside_function = False
        current_function = None

        root_dir = os.path.dirname(self.file)
        relative_dir = root_dir.replace(os.getcwd(), "")
        base_name = os.path.basename((self.file))

        # open and read the file as text lines
        with open(self.file, "r") as file:
            lines = file.readlines()

            for idx, line in enumerate(lines, start=1):
                # checking for function definition
                func_match = re.match(r"def (\w+)\(", line)
                class_match = re.match(r"class (\w+)\(", line)

                # If another function or class is declared, reset the current function
                if func_match or class_match:
                    current_function = None
                if func_match:
                    current_function = func_match.group(1)
                if class_match:
                    current_function = class_match.group(1) + " (class)"

                # check for TODOs
                todo_match = re.search(r"#\s*TODO[^\n]*", line)
                if todo_match:
                    todo = {
                        "dir_path": relative_dir,
                        "file_name": base_name,
                        "line": idx,
                        "function": current_function,
                        "todo": todo_match.group().strip(),
                    }
                    todos.append(todo)
        return todos
