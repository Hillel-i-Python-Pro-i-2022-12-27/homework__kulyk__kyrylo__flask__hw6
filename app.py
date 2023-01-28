from flask import Flask, Response
from webargs import fields
from webargs.flaskparser import use_args

from application.body_application.create_files_txt import to_create_file_txt
from application.body_application.csv_processing import to_calculation_average
from application.body_application.generators import generate_users
from application.body_application.read_files import to_read_file_txt
from application.requests_example.requests_data import to_requests_data, to_download_file
from application.requests_example.response_processing import to_processing_response
from application.services.create_table import create_table
from application.services.db_connection import DBConnect

app = Flask(__name__)


@app.route("/")
def hello_world() -> str:
    return """
    <title>Flask Application</title>
    <h1>Homework 6:</h1>
    <a href=/read_file class="page-to">Task 1 - Reading file. »</a>
    <h3></h3>
    <a href=/users class="page-to">Task 2 - List of users. »</a>
    <h3></h3>
    <a href=/astronauts class="page-to">Task 3 - List of astronauts. »</a>
    <h3></h3>
    <a href=/calculate class="page-to">Task 4 - Calculate average values from CSV-file. »</a>
    <h1>Homework 7:</h1>
    <h3>DB created!</h3>
    <a href=/contacts/read-all class="page-to">Read all contacts. »</a>
    <h3>FAQ:</h3>
    <h4>Add a contact to DB-> /contacts/create?contact_name=&phone_value=</h4>
    <h4>Read a specific contact-> /contacts/read/<u>number</u></h4>
    <h4>Update a specific contact-> /contacts/update/<u>number</u>?contact_name=&phone_value=</h4>
    <h4>Delete a contact-> /contacts/delete/<u>number</u></h4>
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
    <h4>The number of users in the list can be changed by adding to the link "...?amount=number", default amount=10</h4>
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


@app.route("/contacts/create")
@use_args({"contact_name": fields.Str(required=True), "phone_value": fields.Int(required=True)}, location="query")
def contact__create(args):
    with DBConnect() as connection:
        with connection:
            connection.execute(
                "INSERT INTO phones (contact_name, phone_value) VALUES (:contact_name, :phone_value);",
                {"contact_name": args["contact_name"], "phone_value": args["phone_value"]},
            )
    return """
    Successful! Information added to the DB.
    <h3></h3>
    <a href=/ class='page-to'>To the main »
    """


@app.route("/contacts/read-all")
def contact__read__all():
    with DBConnect() as connection:
        contacts = connection.execute("SELECT * FROM phones;").fetchall()
    return f"""
    {"<br>".join(
        [f'{contact["phone_id"]}: {contact["contact_name"]} - {contact["phone_value"]}' for contact in contacts]
    )}
    <h3></h3>
    <a href=/ class='page-to'>To the main »
    """


@app.route("/contacts/read/<int:phone_id>")
def contact__read(phone_id: int):
    with DBConnect() as connection:
        contact = connection.execute(
            "SELECT * " "FROM phones " "WHERE (phone_id=:phone_id);",
            {
                "phone_id": phone_id,
            },
        ).fetchone()
    return f"""
    {contact["phone_id"]}: {contact["contact_name"]} - {contact["phone_value"]}
    <h3></h3>
    <a href=/ class='page-to'>To the main »
    """


@app.route("/contacts/update/<int:phone_id>")
@use_args({"contact_name": fields.Str(), "phone_value": fields.Int()}, location="query")
def contact__update(args, phone_id: int):
    with DBConnect() as connection:
        with connection:
            contact_name = args.get("contact_name")
            phone_value = args.get("phone_value")
            if contact_name is None and phone_value is None:
                return Response(
                    "You did not provide any argument to update the contact!",
                    status=400,
                )
            args_for_request = []
            if contact_name is not None:
                args_for_request.append("contact_name=:contact_name")
            if phone_value is not None:
                args_for_request.append("phone_value=:phone_value")
            args_2 = ", ".join(args_for_request)
            connection.execute(
                "UPDATE phones " f"SET {args_2} " "WHERE phone_id=:phone_id;",
                {
                    "phone_id": phone_id,
                    "contact_name": contact_name,
                    "phone_value": phone_value,
                },
            )
    return """
    Successful! Information updated to the DB.
    <h3></h3>
    <a href=/ class='page-to'>To the main »
    """


@app.route("/contacts/delete/<int:phone_id>")
def contact__delete(phone_id):
    with DBConnect() as connection:
        with connection:
            connection.execute(
                "DELETE " "FROM phones " "WHERE (phone_id=:phone_id);",
                {
                    "phone_id": phone_id,
                },
            )
    return """
    Deletion successful!
    <h3></h3>
    <a href=/ class='page-to'>To the main »
    """


create_table()

if __name__ == "__main__":
    app.run()
