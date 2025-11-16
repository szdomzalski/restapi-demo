from datetime import datetime, timezone
from marshmallow_sqlalchemy import fields

from config import db, ma


class Note(db.Model):
    """
    Note Model for storing notes associated with a person
    """
    __tablename__ = "note"

    id: int = db.Column(db.Integer, primary_key=True)
    person_id: int = db.Column(db.Integer, db.ForeignKey("person.id"))
    content: str = db.Column(db.String, nullable=False)
    timestamp: datetime = db.Column(
        db.DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc)
    )


class NoteSchema(ma.SQLAlchemyAutoSchema):
    """
    Note Schema for serialization/deserialization
    """
    class Meta:
        model = Note
        load_instance = True
        sqla_session = db.session
        include_fk = True
        # Convert datetime to ISO format string
        datetime_format = "%Y-%m-%dT%H:%M:%S.%fZ"


class ReadNoteSchema(ma.SQLAlchemyAutoSchema):
    """
    Note Schema for reading notes (limited fields)
    """
    class Meta:
        model = Note
        load_instance = True
        sqla_session = db.session
        include_fk = False  # I do not want to include person_id in the serialized output
        fields = ("content", "timestamp")  # Only include content and timestamp fields
        # Convert datetime to ISO format string
        datetime_format = "%Y-%m-%dT%H:%M:%S.%fZ"


class Person(db.Model):
    """
    Person Model for storing user information
    """
    __tablename__ = "person"

    id: int = db.Column(db.Integer, primary_key=True)
    lname: str = db.Column(db.String(32))
    fname: str = db.Column(db.String(32))
    timestamp: datetime = db.Column(
        db.DateTime(timezone=True),  # Use timezone-aware datetime
        default=lambda: datetime.now(timezone.utc),  # Default to current UTC time
        onupdate=lambda: datetime.now(timezone.utc)  # Update timestamp on record modification
    )
    notes = db.relationship(  # Create new attribute 'notes' for relationship
        Note,  # Linking to Note model ("notes" table)
        backref="person",  # Back-reference to access Person from Note
        cascade="all, delete, delete-orphan",  # Cascade delete notes when person is deleted
        single_parent=True,  # Ensure each Note has only one parent Person
        order_by="desc(Note.timestamp)"  # Order notes by timestamp descending
    )

    def __repr__(self) -> str:
        """Return a string representation of the Person."""
        return f"<Person {self.fname} {self.lname}>"

    def to_dict(self) -> dict:
        """Convert Person object to dictionary."""
        return {
            "id": self.id,
            "lname": self.lname,
            "fname": self.fname,
            "timestamp": self.timestamp.isoformat()
        }

    @staticmethod
    def from_dict(data: dict) -> "Person":
        """Create Person object from dictionary."""
        return Person(
            lname=data.get("lname"),
            fname=data.get("fname")
        )

class PersonSchema(ma.SQLAlchemyAutoSchema):
    """
    Person Schema for serialization/deserialization
    """
    # SQLAlchemyAutoSchema automatically generates fields based on the model specified in Meta
    class Meta:
        model = Person
        load_instance = True  # Deserialize JSON to model instances
        sqla_session = db.session  # Use the SQLAlchemy session
        include_fk = True  # Include foreign keys
        include_relationships = True  # Include relationships like 'notes'
        # Convert datetime to ISO format string
        datetime_format = "%Y-%m-%dT%H:%M:%S.%fZ"

    notes = fields.Nested(ReadNoteSchema, many=True)  # Nested field for related notes

# Initialize schemas for single object and collections
person_schema = PersonSchema()
people_schema = PersonSchema(many=True)  # Expect iterable of Person objects
note_schema = NoteSchema()
# notes_schema = NoteSchema(many=True)  # Expect iterable of Note objects