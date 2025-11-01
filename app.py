from flask import render_template
import connexion


# app = Flask(__name__)
app = connexion.FlaskApp(__name__, specification_dir='./')
app.add_api('openapi.yaml')

@app.route('/')
def home() -> str:
    return render_template('index.html')


if __name__ == '__main__':
    app.app.debug = True  # Set debug mode on the underlying Flask app
    app.run()