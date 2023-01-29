from application.body_application.generators import generate_text
from application.config.paths import FILES_INPUT_PATH
from application.logging.loggers import get_core_logger


def to_create_file_txt(name_file: str = None) -> None:
    logger = get_core_logger()
    path_to_file = FILES_INPUT_PATH.joinpath(f"{name_file}.txt")
    with open(path_to_file, mode="w") as file:
        file.write(f"{generate_text()}")
    logger.info(f"Path to file: {path_to_file}")
