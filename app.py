from flask import Flask
from webargs import fields
from webargs.flaskparser import use_args

from application.body_application.create_files_txt import to_create_file_txt
from application.body_application.generators import generate_users
from application.body_application.read_files import to_read_file_txt

app = Flask(__name__)


@app.route("/")
def hello_world():
    profile_1 = "/read_file"
    profile_2 = "/users"
    return f"""
    <title>Flask Application</title>
    <h1>Homework tasks:</h1>
    <a href={profile_1} class="page-to">Task 1 - Reading file. »
    <h2></h2>
    <a href={profile_2} class="page-to">Task 2 - List of users. »
    <h2></h2>
    <a href={profile_2} class="page-to">Task 2 - List of users. »
    """


@app.route("/read_file")
def to_read_fila_txt():
    to_create_file_txt("user")
    read_file = to_read_file_txt("user")
    profile = "/"
    # output = ''.join(<f"{read_file}"
    # )
    return f"""
    <h2>Text from user.txt:</h2>
    <span>{read_file}</span>
    <h2></h2>
    <a href={profile} class='page-to'>To the main »
    """


@app.route("/users")
@use_args({"amount": fields.Int(missing=10)}, location="query")
def to_generate_users(args):
    amount = args["amount"]
    users = generate_users(amount=amount)
    profile = "/"
    output = "".join(
        f"<li>" f"<span>{User.name}</span>" f"<span> - </span>" f"<span>{User.email}</span>" f"</li>" for User in users
    )
    return f"""
    <h3>Users:</h3>
    <ol>{output}</ol>
    <h2></h2>
    <a href={profile} class='page-to'>To the main »
    """


if __name__ == "__main__":
    app.run()
