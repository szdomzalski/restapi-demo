from flask import render_template

import config
from models import Person


# app = Flask(__name__)
app = config.connexion_app
app.add_api(config.basedir / 'openapi.yaml')

@app.route('/')
def home() -> str:
    people = Person.query.all()
    return render_template('index.html', people=people)


if __name__ == '__main__':
    app.app.debug = True  # Set debug mode on the underlying Flask app
    app.run()