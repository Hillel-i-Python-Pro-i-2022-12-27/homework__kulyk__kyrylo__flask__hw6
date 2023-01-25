from application.body_application.generators import generate_users
from application.config.paths import FILES_OUTPUT_PATH
from application.logging.loggers import get_core_logger


def to_write_file_txt(name_file: str = None, amount_users: int = 100) -> None:
    logger = get_core_logger()
    path_to_file = FILES_OUTPUT_PATH.joinpath(f"{name_file}.txt")
    with open(path_to_file, mode="w") as file:
        for user in generate_users(amount=amount_users):
            file.write(f"{user.name} {user.email}\n")
    logger.info(f"Path to file: {path_to_file}")


if __name__ == "__main__":
    to_write_file_txt()
