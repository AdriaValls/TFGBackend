from datetime import datetime

from models.match import MatchModel
from flask_restful import Resource, reqparse


# Account actions (register, update, delete)
class Match(Resource):

    def get(self, id):
        match = MatchModel.get_by_id(id)
        if match:
            return {"match": match.json()}, 200
        return {"message": f"Could not find an a match with that id"}, 404

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument("title", type=str, required=True, nullable=False)
        parser.add_argument("description", type=str, required=False, nullable=False, default="")

        data = parser.parse_args()

        try:
            new_match = MatchModel(
                data["title"],
                data["description"],
            )
            new_match.save_to_db()

        except Exception:
            return {"message": "An error occurred creating the match."}, 500

        return {"match": new_match.json()}, 201
