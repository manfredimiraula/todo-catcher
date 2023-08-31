import logging
import os
from datetime import datetime

# TODO use `pathlib`` instead of `os`


class Logger:
    """
    A simple logging class that creates a new log file for each run, using the current date and time as part of the
    filename. Logs are written to a specified directory.
    """

    def __init__(self, log_dir: str, name: str, level: int = logging.INFO):
        """
        Initializes a new Logger object.

        Parameters
        ----------
        log_dir : str
            Directory where log files should be written.
        name : str
            Name of the logger.
        level : int, optional
            Logging level. Defaults to logging.INFO.
            Levels:
            - DEBUG: Detailed information, typically of interest only when diagnosing problems.
            - INFO: Confirmation that things are working as expected.
            - WARNING: An indication that something unexpected happened,
                or may happen in the near future.
            - ERROR: The software has not been able to perform some function.
            - CRITICAL: A very serious error, indicating that the program
                itself may be unable to continue running.
        """
        self.logger = logging.getLogger(name)
        self.logger.setLevel(level)

        if not os.path.exists(log_dir):
            os.makedirs(log_dir)

        log_file_name = f"{name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"
        file_handler = logging.FileHandler(os.path.join(log_dir, log_file_name))
        file_handler.setFormatter(
            logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
        )

        self.logger.addHandler(file_handler)

    def get_logger(self) -> logging.Logger:
        """
        Returns the logger object for this Logger.

        Returns
        -------
        logger : logging.Logger
            The logger object.
        """
        return self.logger
