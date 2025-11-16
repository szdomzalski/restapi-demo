from email.policy import HTTP
from flask import abort, make_response
from http import HTTPStatus

from config import db
from models import Note, Person, note_schema


def read_one(note_id: int) -> dict[str, str]:
    note = Note.query.get(note_id)  # Use get() for primary key lookup as note_id is primary key

    if note is not None:
        return note_schema.dump(note)
    else:
        abort(HTTPStatus.NOT_FOUND, f'Note with ID {note_id} not found')


def update(note_id: int, note: str) -> tuple[dict[str, str], int]:
    existing_note = Note.query.get(note_id)

    if existing_note is None:
        abort(HTTPStatus.NOT_FOUND, f'Note with ID {note_id} not found')

    update_note = note_schema.load(note, session=db.session)
    existing_note.content = update_note.content
    db.session.merge(existing_note)
    db.session.commit()
    return note_schema.dump(existing_note), HTTPStatus.OK


def delete(note_id: int) -> tuple[str, int]:
    existing_note = Note.query.get(note_id)

    if existing_note is None:
        abort(HTTPStatus.NOT_FOUND, f'Note with ID {note_id} not found')

    db.session.delete(existing_note)
    db.session.commit()
    return make_response(f'{note_id} successfully deleted', HTTPStatus.NO_CONTENT)


def create(note: dict[str, str]) -> tuple[dict[str, str], int]:
    person_id = note["person_id"]
    person = Person.query.get(person_id)

    if person is None:
        abort(HTTPStatus.NOT_FOUND, f'Person not found for ID: {person_id}')

    new_note = note_schema.load(note, session=db.session)
    person.notes.append(new_note)
    db.session.commit()
    return note_schema.dump(new_note), HTTPStatus.CREATED

