import pathlib
import connexion
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

basedir = pathlib.Path(__file__).parent.resolve()  # Localize the base app directory
# Create Connexion app instance, pointing to base dir for OpenAPI spec
connexion_app = connexion.FlaskApp(__name__, specification_dir=basedir)

app = connexion_app.app
# Configure sqlite database
app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{basedir / 'people.db'}"
# Disable event system to save resources as this is not event-driven app (unnecessary overhead)
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)
ma = Marshmallow(app)
