import time

from db import db
from flask import current_app, g

from flask_httpauth import HTTPTokenAuth
from jwt import ExpiredSignatureError, InvalidSignatureError, decode, encode
from passlib.apps import custom_app_context as pwd_context

auth = HTTPTokenAuth(scheme="Bearer")


class UserModel(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(30), unique=True, nullable=False)
    password = db.Column(db.String(), nullable=False)
    email = db.Column(db.String(30), unique=True, nullable=False)
    description = db.Column(db.String(200), nullable=False)
    is_admin = db.Column(db.Integer, nullable=False)

    owned_matches = db.relationship("MatchModel", back_populates="owner", cascade="all, delete-orphan")

    def __init__(self, username, email, description, is_admin):
        self.username = username
        self.email = email
        self.description = description
        self.is_admin = is_admin

    def json(self):
        return {
            "id": self.id,
            "username": self.username,
            "email": self.email,
            "description": self.description,
            "is_admin": self.is_admin,
        }

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()

    def rollback(self):
        db.session.rollback(self)
        db.session.commit()

    @classmethod
    def get_by_id(cls, id):
        return cls.query.filter_by(id=id).first()

    @classmethod
    def get_by_username(cls, username):
        return cls.query.filter_by(username=username).first()

    @classmethod
    def get_by_email(cls, email):
        return cls.query.filter_by(email=email).first()

    @classmethod
    def get_all(cls):
        return cls.query.all()

    # Password Stuff
    def hash_password(self, password):
        self.password = pwd_context.hash(password)

    def verify_password(self, password):
        return pwd_context.verify(password, self.password)

    def generate_auth_token(self, expiration=6000):
        return encode(
            {"username": self.username, "exp": int(time.time()) + expiration},
            current_app.secret_key,
            algorithm="HS256",
        )

    @classmethod
    def verify_auth_token(cls, token):
        try:
            data = decode(token, current_app.secret_key, algorithms=["HS256"])
        except ExpiredSignatureError:
            return None  # expired token
        except InvalidSignatureError:
            return None  # invalid token
        except Exception:
            return None  # bad token (e.g. DecodeError)

        user = cls.query.filter_by(username=data["username"]).first()
        return user

    @auth.verify_token
    def verify_token(token):
        user = UserModel.verify_auth_token(token)
        if user is not None:
            g.user = user
        else:
            g.user = None
        return user

    # User role
    @auth.get_user_roles
    def get_user_roles(user):
        roles = ["user"]
        if user.is_admin:
            roles.append("admin")
        return roles
