from models.user import UserModel
from flask_restful import Resource, reqparse


# Account actions (register, update, delete)
class Account(Resource):

    def get(self, id):
        match = UserModel.get_by_id(id)
        if match:
            return {"match": match.json()}, 200
        return {"message": f"Could not find an a match with that id"}, 404

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument("username", type=str, required=True, nullable=False)
        parser.add_argument("password", type=str, required=True, nullable=False)
        parser.add_argument("email", type=str, required=True, nullable=False)
        parser.add_argument("description", type=str, required=False, nullable=False, default="")
        parser.add_argument("is_admin", type=int, required=False, nullable=False, default=0)

        data = parser.parse_args()

        if UserModel.get_by_username(data["username"]):
            return {"message": "An account with this username already exists!"}, 409
        if UserModel.get_by_email(data["email"]):
            return {"message": "An account with this email already exists!"}, 409
        try:
            new_match = UserModel(
                data["username"],
                data["password"],
                data["email"],
                data["description"],
                data["is_admin"]
            )
            new_match.save_to_db()

        except Exception:
            return {"message": f"Could not create user"}, 500

        return {"user": new_match.json()}, 201
