from datetime import datetime, timezone
from config import db, ma

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
        sqla_session = db.session
        # Include all fields by default
        include_fk = True
        # Convert datetime to ISO format string
        datetime_format = "%Y-%m-%dT%H:%M:%S.%fZ"

# Initialize schemas for single object and collections
person_schema = PersonSchema()
people_schema = PersonSchema(many=True)  # Expect iterable of Person objects