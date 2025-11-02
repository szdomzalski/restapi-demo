from math import e
from flask import abort
from http import HTTPStatus

from config import db
from models import Person, person_schema, people_schema


def read_all() -> list[dict[str, str]]:
    people = Person.query.all()
    dumpy = people_schema.dump(people)
    print(type(dumpy))
    return people_schema.dump(people)


def create(person: dict[str, str]) -> tuple[dict[str, str], int]:
    lname = person['lname']  # Required field

    if not lname:
        abort(HTTPStatus.BAD_REQUEST, "Last name is required")

    if Person.query.filter_by(lname=lname).one_or_none() is not None:
        abort(HTTPStatus.CONFLICT, f"Person with last name '{lname}' already exists")

    new_person = person_schema.load(person, session=db.session)  # We can directly load payload into Person model
    db.session.add(new_person)
    db.session.commit()
    return person_schema.dump(new_person), HTTPStatus.CREATED


def read_one(lname: str) -> dict[str, str]:
    person = Person.query.filter_by(lname=lname).one_or_none()
    if person is not None:
        return person_schema.dump(person)
    else:
        abort(HTTPStatus.NOT_FOUND, f'Person with last name {lname} not found')


def update(lname: str, person: dict[str, str]) -> dict[str, str]:
    existing_person = Person.query.filter_by(lname=lname).one_or_none()
    if existing_person is None:
        abort(HTTPStatus.NOT_FOUND, f'Person with last name {lname} not found')

    updated_person = person_schema.load(person, session=db.session)
    existing_person.fname = updated_person.fname
    db.session.commit()
    return person_schema.dump(existing_person), HTTPStatus.OK


def delete(lname: str) -> tuple[str, int]:
    existing_person = Person.query.filter_by(lname=lname).one_or_none()
    if existing_person is None:
        abort(HTTPStatus.NOT_FOUND, f'Person with last name {lname} not found')

    db.session.delete(existing_person)
    db.session.commit()
