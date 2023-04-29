from db import db
from datetime import datetime
from flask_httpauth import HTTPTokenAuth

auth = HTTPTokenAuth(scheme="Bearer")


class MatchModel(db.Model):

    __tablename__ = "matches"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(280), unique=False, nullable=False)
    description = db.Column(db.String(280), unique=False, nullable=False)
    location = db.Column(db.String(280), unique=False, nullable=False)
    city = db.Column(db.String(280), unique=False, nullable=False)
    date = db.Column(db.String(280), nullable=False)
    numPlayers = db.Column(db.Integer, unique=False, nullable=False)
    sport = db.Column(db.String(), unique=False, nullable=False)
    ongoing = db.Column(db.Boolean, unique=False, nullable=False, default=True)
    owner_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)

    owner = db.relationship("UserModel", foreign_keys=[owner_id], back_populates="owned_matches")

    def __init__(self, title, description, location, city, date, numplayers, sport, ongoing):
        self.title = title
        self.description = description
        self.location = location
        self.city = city
        self.date = date
        self.numPlayers = numplayers
        self.sport = sport
        self.ongoing = ongoing

    def json(self):
        return {
            "title": self.title,
            "description": self.description,
            "location": self.location,
            "city": self.city,
            "date": self.date,
            "numPlayers": self.numPlayers,
            "sport": self.sport,
            "ongoing": self.ongoing,
            "owner_id": self.owner_id
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
    def get_by_sport(cls, sport):
        return cls.query.filter_by(sport=sport).first()

    @classmethod
    def get_by_city(cls, city):
        return cls.query.filter_by(city=city).first()

    @classmethod
    def get_all(cls):
        return cls.query.all()

    @classmethod
    def get_owned_by_account(cls, user_id, amount, offset):
        q = cls.query.filter_by(owner_id=user_id)
        return q.limit(amount).offset(offset).all()
    #q.order_by(cls.time.desc()).limit(amount).offset(offset).all()