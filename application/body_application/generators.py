from collections.abc import Iterator
from random import randint
from faker import Faker
from application.body_application.class_for_gererators import User

fake = Faker()


def generate_user() -> User:
    fake_name = fake.first_name()
    return User(name=fake_name, email=f"{fake_name.lower()}.{randint(1000, 9999)}@{fake.domain_name()}")


def generate_users(amount) -> Iterator[User]:
    for _ in range(amount):
        yield generate_user()


def generate_text() -> Faker:
    return fake.text().replace(". ", ".\n")
