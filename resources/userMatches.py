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

