import flask

from app_files.models import db

app = flask.Flask(__name__)

# Configure the app to use SQLite database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///recipe_app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

db.init_app(app)

def getApp():
    return app