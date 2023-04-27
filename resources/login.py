from models.user import UserModel, auth, g
from flask_restful import Resource, reqparse


class Login(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument("username", type=str, required=True, nullable=False)
    parser.add_argument("password", type=str, required=True, nullable=False)

    def post(self):
        data = self.parser.parse_args()
        username = data["username"]
        password = data["password"]

        account = UserModel.get_by_username(username)
        if not account:
            return {"message": f"Login failed! No account was found with username: {username}"}, 404

        if not account.verify_password(password):
            return {"message": "Invalid password!"}, 404

        token = account.generate_auth_token()
        return {"token": token}, 200