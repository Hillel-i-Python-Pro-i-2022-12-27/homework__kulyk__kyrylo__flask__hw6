from flask import Flask
from webargs import fields
from webargs.flaskparser import use_args

from application.body_application.create_files_txt import to_create_file_txt
from application.body_application.csv_processing import to_calculation_average
from application.body_application.generators import generate_users
from application.body_application.read_files import to_read_file_txt
from application.requests_example.requests_data import to_requests_data, to_download_file
from application.requests_example.response_processing import to_processing_response

app = Flask(__name__)


@app.route("/")
def hello_world() -> str:
    return """
    <title>Flask Application</title>
    <h1>Homework tasks:</h1>
    <a href=/read_file class="page-to">Task 1 - Reading file. »
    <h2></h2>
    <a href=/users class="page-to">Task 2 - List of users. »
    <h2></h2>
    <a href=/astronauts class="page-to">Task 3 - List of astronauts. »
    <h2></h2>
    <a href=/calculate class="page-to">Task 4 - Calculate average values from CSV-file. »
    """


@app.route("/read_file")
def to_read_fila_txt() -> str:
    to_create_file_txt(name_file="fake_text")
    read_file = to_read_file_txt(name_file="fake_text")
    return f"""
    <h2>Text from fake_text.txt:</h2>
    <span>{read_file}</span>
    <h3></h3>
    <a href=/ class='page-to'>To the main »
    """


@app.route("/users")
@use_args({"amount": fields.Int(missing=10)}, location="query")
def to_generate_users(args) -> str:
    amount = args["amount"]
    users = generate_users(amount=amount)
    output = "".join(
        f"<li>" f"<span>{User.name}</span>" f"<span> - </span>" f"<span>{User.email}</span>" f"</li>" for User in users
    )
    return f"""
    <h3>Users:</h3>
    <ol>{output}</ol>
    <h3></h3>
    <a href=/ class='page-to'>To the main »
    """


@app.route("/astronauts")
def to_get_info_astronauts() -> str:
    to_requests_data(url="http://api.open-notify.org/astros.json")
    return f"""
    <h3>List of astronauts:</h3>
    <span>The number of people in space at this moment:</span>
    <h3></h3>
    <span>{to_processing_response(name_file="output")}-astronauts</span>
    <h3></h3>
    <a href=/ class='page-to'>To the main »
    """


@app.route("/calculate")
def to_get_average_values() -> str:
    to_download_file(url="https://drive.google.com/u/0/uc?id=1kQ8mFcgGpGK4XRtnWQdWf-y10Ru2UQdB&export=download")
    average_values = to_calculation_average(name_file="output")
    return f"""
    <h3>After processing the csv-file, we got the following values:</h3>
    <span>Average height of people: {average_values["average_height_in_cm"]} cm.</span>
    <h3></h3>
    <span>Average weight of people: {average_values["average_weight_in_kg"]} kg.</span>
    <h3></h3>
    <a href=/ class='page-to'>To the main »
    """


if __name__ == "__main__":
    app.run()
