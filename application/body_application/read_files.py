from application.config.paths import FILES_INPUT_PATH


def to_read_file_txt(name_file: str = None) -> None:
    path_to_file = FILES_INPUT_PATH.joinpath(f"{name_file}.txt")
    file_contents = path_to_file.read_text()
    print(file_contents)


if __name__ == "__main__":
    to_read_file_txt()
