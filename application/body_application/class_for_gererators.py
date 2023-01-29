from typing import NamedTuple


class User(NamedTuple):
    name: str
    email: str

    def __str__(self):
        return f"{self.name} {self.email}"

    __repr__ = __str__
