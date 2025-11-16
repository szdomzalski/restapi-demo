from datetime import datetime

from config import app, db
from models import Person, Note


# Some initial people with associated notes
PEOPLE_NOTES = [
    {
        "lname": "Fairy",
        "fname": "Tooth",
        "notes": [
            ("I brush my teeth after each meal.", "2022-01-06 17:10:24"),
            ("The other day a friend said, I have big teeth.", "2022-03-05 22:17:54"),
            ("Do you pay per gram?", "2022-03-05 22:18:10"),
        ],
    },
    {
        "lname": "Ruprecht",
        "fname": "Knecht",
        "notes": [
            ("I swear, I'll do better this year.", "2022-01-01 09:15:03"),
            ("Really! Only good deeds from now on!", "2022-02-06 13:09:21"),
        ],
    },
    {
        "lname": "Bunny",
        "fname": "Easter",
        "notes": [
            ("Please keep the current inflation rate in mind!", "2022-01-07 22:47:54"),
            ("No need to hide the eggs this time.", "2022-04-06 13:03:17"),
        ],
    },
]


def init_database() -> None:
    """Initialize the database with some initial data.
    Returns: None
    """
    with app.app_context():
        db.create_all()  # Create tables based on models
        for person_data in PEOPLE_NOTES:
            person = Person(
                lname=person_data["lname"],
                fname=person_data["fname"]
            )
            db.session.add(person)
            db.session.flush()  # Flush to get person.id for foreign key

            for note_content, note_timestamp in person_data["notes"]:
                note = Note(
                    person_id=person.id,
                    content=note_content,
                    timestamp=datetime.fromisoformat(note_timestamp)
                )
                db.session.add(note)

        db.session.commit()


if __name__ == '__main__':
    init_database()