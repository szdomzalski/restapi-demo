from datetime import datetime
from flask import abort
from http import HTTPStatus


def get_timestamp() -> str:
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


MOCK_PEOPLE = {
    "fairy": {
        "fname": "Tooth",
        "lname": "Fairy",
        "timestamp": get_timestamp(),
    },
    "ruprecht": {
        "fname": "Knecht",
        "lname": "Ruprecht",
        "timestamp": get_timestamp(),
    },
    "bunny": {
        "fname": "Easter",
        "lname": "Bunny",
        "timestamp": get_timestamp(),
    }
}


def read_all() -> list[dict[str, str]]:
    return [*MOCK_PEOPLE.values()]


def create(person: dict[str, str]) -> tuple[dict[str, str], int]:
    lname = person['lname']  # Required field
    fname = person.get("fname", "")

    if not lname:
        abort(HTTPStatus.BAD_REQUEST, "Last name is required")

    last_name_insensitive = lname.casefold()

    if last_name_insensitive in MOCK_PEOPLE:
        abort(HTTPStatus.CONFLICT, f"Person with last name '{lname}' already exists")

    MOCK_PEOPLE[last_name_insensitive] = {
        "lname": lname,
        "fname": fname,
        "timestamp": get_timestamp(),
    }
    return MOCK_PEOPLE[last_name_insensitive], HTTPStatus.CREATED


def read_one(lname: str) -> dict[str, str]:
    lname_insensitive = lname.casefold()
    try:
        return MOCK_PEOPLE[lname_insensitive]
    except KeyError:
        abort(HTTPStatus.NOT_FOUND, f'Person with last name {lname} not found')


def update(lname: str, person: dict[str, str]) -> dict[str, str]:
    lname_insensitive = lname.casefold()
    try:
        MOCK_PEOPLE[lname_insensitive]['fname'] = person.get('fname', MOCK_PEOPLE[lname_insensitive]['fname'])
        MOCK_PEOPLE[lname]["timestamp"] = get_timestamp()
        return MOCK_PEOPLE[lname_insensitive]
    except KeyError:
        abort(HTTPStatus.NOT_FOUND, f'Person with last name {lname} not found')


def delete(lname: str) -> tuple[str, int]:
    lname_insensitive = lname.casefold()
    try:
        del MOCK_PEOPLE[lname_insensitive]
        return None, HTTPStatus.NO_CONTENT
    except KeyError:
        abort(HTTPStatus.NOT_FOUND, f'Person with last name {lname} not found')
