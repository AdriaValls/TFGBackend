from models.user import UserModel, auth, g
from models.match import MatchModel
from flask_restful import Resource, reqparse


class OwnedMatches(Resource):

    @auth.login_required()
    def get(self, id):
        owner = UserModel.get_by_id(id)
        if owner:
            matches = MatchModel.get_owned_by_account(id, 20, 0)
            if matches:
                return {"owned_matches": [match.json() for match in matches]}, 200
            return {"message": f"User has no owned matches"}, 404
        return {"message": f"User does not exist"}, 404


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
            owner = UserModel.get_by_username(g.user.username)
            new_match.owner = owner

            new_match.save_to_db()

        except Exception:
            return {"message": "An error occurred creating the match."}, 500

        return {"match": new_match.json()}, 201

