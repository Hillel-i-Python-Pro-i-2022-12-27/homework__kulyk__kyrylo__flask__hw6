from application.config.paths import FILES_INPUT_PATH


def to_read_file_txt(name_file: str = None) -> str:
    path_to_file = FILES_INPUT_PATH.joinpath(f"{name_file}.txt")
    return path_to_file.read_text()


if __name__ == "__main__":
    to_read_file_txt()
