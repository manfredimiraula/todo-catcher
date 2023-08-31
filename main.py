from src.utils.misc import scan_directory
from src.utils.logging import Logger


log_dir = ".logs/testing"
logger = Logger(log_dir, name="31_08_2023")

if __name__ == "__main__":
    # ask to specify a directory
    directory = str(
        input("Enter directory path (or press enter to scan current root directory): ")
    ).strip()

    directory = directory if directory else None
    logger.logger.info(f"Catching TODOs in {directory}")
    print(f"Catching TODOs in {directory}")

    todos = scan_directory(logger, directory)
    logger.logger.info(f"{len(todos)} found. Continue processing...")
    print(f"{len(todos)} found. Continue processing...")

    output = str(
        input("Set 'm' to write an .md file; chose 'n' to write to a Notion page")
    )

    if output == "m":
        print("writing to .md")
    elif output == "n":
        print("writing to Notion page")
