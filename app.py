from flask import Flask
from flask_cors import CORS
from flask_migrate import Migrate
from flask_restful import Api
from db import db
from data import matches, users

from models.match import MatchModel

from resources.accounts import Account
from resources.matches import Match

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'

api = Api(app)

migrate = Migrate(app, db)
db.init_app(app)

api.add_resource(Account, "/account")
api.add_resource(Match, "/match/<int:id>", "/match")

@app.route('/')
def hello_world():  # put application's code here
    return 'Hello World!'


if __name__ == '__main__':
    app.run()
