from db import db
from flask import current_app, g


class UserModel(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(30), unique=True, nullable=False)
    password = db.Column(db.String(), nullable=False)
    email = db.Column(db.String(30), unique=True, nullable=False)
    description = db.Column(db.String(200), nullable=False)
    is_admin = db.Column(db.Integer, nullable=False)

    def __init__(self, username, password, email, description, is_admin):
        self.username = username
        self.password = password
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