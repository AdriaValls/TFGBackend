from datetime import datetime

from models.user import UserModel, auth, g
from models.match import MatchModel
from flask_restful import Resource, reqparse


# Account actions (register, update, delete)


class Match(Resource):

    def get(self, id):
        match = MatchModel.get_by_id(id)
        if match:
            return {"match": match.json()}, 200
        return {"message": f"Could not find an a match with that id"}, 404

    # Post New Match
    @auth.login_required()
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument("title", type=str, required=True, nullable=False)
        parser.add_argument("description", type=str, required=False, nullable=False, default="")
        parser.add_argument("location", type=str, required=True, nullable=False)
        parser.add_argument("city", type=str, required=True, nullable=False)
        parser.add_argument("date", type=str, required=True, nullable=False)
        parser.add_argument("numPlayers", type=int, required=True, nullable=False)
        parser.add_argument("sport", type=str, required=True, nullable=False)
        parser.add_argument("ongoing", type=bool, required=True, nullable=False)
        data = parser.parse_args()

        try:
            new_match = MatchModel(
                data["title"],
                data["description"],
                data["location"],
                data["city"],
                data["date"],
                data["numPlayers"],
                data["sport"],
                data["ongoing"],
            )
            acc = UserModel.get_by_username(g.user.username)

            new_match.save_to_db()

        except Exception:
            return {"message": "An error occurred creating the match."}, 500

        return {"match": new_match.json(), "acc": acc.json()}, 201

    @auth.login_required()
    def delete(self, id):
        try:
            account = MatchModel.get_by_id(id)
            account.delete_from_db()
        except Exception:
            return {"message": "An error occurred deleting the account."}, 500
        return {"message": "Account deleted successfully!"}, 200