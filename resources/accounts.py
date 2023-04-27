from models.user import UserModel, auth, g
from flask_restful import Resource, reqparse


# Account actions (register, update, delete)
class Account(Resource):

    @auth.login_required()
    def get(self, user_id):
        match = UserModel.get_by_id(user_id)
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
            new_account = UserModel(
                data["username"],
                data["email"],
                data["description"],
                data["is_admin"]
            )
            new_account.hash_password(data["password"])
            new_account.save_to_db()

        except Exception:
            return {"message": f"Could not create user"}, 500

        return {"user": new_account.json()}, 201

    # Delete user
    @auth.login_required()
    def delete(self, username):
        if username is None:
            return {"message": "No username specified."}, 400
        if username != g.user.username:
            return {"message": "You can't delete someone else's account."}, 403
        account = UserModel.get_by_username(username)
        if account is None:
            return {"message": "Could not find an account with that username."}, 404
        try:
            account.delete_from_db()
        except Exception:
            return {"message": "An error occurred deleting the account."}, 500
        return {"message": "Account deleted successfully!"}, 200
