from datetime import datetime
from flask import abort
from http import HTTPStatus


def get_timestamp() -> str:
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


MOCKED_PEOPLE_DATA = {
    "Fairy": {
        "fname": "Tooth",
        "lname": "Fairy",
        "timestamp": get_timestamp(),
    },
    "Ruprecht": {
        "fname": "Knecht",
        "lname": "Ruprecht",
        "timestamp": get_timestamp(),
    },
    "Bunny": {
        "fname": "Easter",
        "lname": "Bunny",
        "timestamp": get_timestamp(),
    }
}


def read_all() -> list[dict[str, str]]:
    return [*MOCKED_PEOPLE_DATA.values()]


def create(person: dict[str, str]) -> tuple[dict[str, str], int]:
    lname = person['lname']  # Required field
    fname = person.get("fname", "")

    if lname and lname not in MOCKED_PEOPLE_DATA:
        MOCKED_PEOPLE_DATA[lname] = {
            "lname": lname,
            "fname": fname,
            "timestamp": get_timestamp(),
        }
        return MOCKED_PEOPLE_DATA[lname], HTTPStatus.CREATED
    else:
        abort(HTTPStatus.NOT_ACCEPTABLE, f'Person with last name {lname} already exists')
