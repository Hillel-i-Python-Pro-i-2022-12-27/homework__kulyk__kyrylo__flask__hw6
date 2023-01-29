import csv

from application.config.paths import FILES_OUTPUT_PATH


def to_calculation_average(name_file: str = None) -> dict:
    path_to_file = FILES_OUTPUT_PATH.joinpath(f"{name_file}.csv")
    with open(path_to_file) as file:
        reader_csv = csv.DictReader(file)
        sum_of_people_height = 0
        sum_of_people_weight = 0
        for line in reader_csv:
            sum_of_people_height += float(line["Height(Inches)"])
            sum_of_people_weight += float(line["Weight(Pounds)"])
        average_height_in_cm = round((sum_of_people_height / int(line["Index"])) * 2.54, 2)
        average_weight_in_kg = round((sum_of_people_weight / int(line["Index"])) * 0.45, 2)
        return {"average_height_in_cm": average_height_in_cm, "average_weight_in_kg": average_weight_in_kg}
