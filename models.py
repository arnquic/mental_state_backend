from re import S
from flask.scaffold import F
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import backref
db = SQLAlchemy()

class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    firstName = db.Column(db.String, nullable=False)
    lastName = db.Column(db.String, nullable=False)
    email = db.Column(db.String, nullable=False, unique=True)
    password = db.Column(db.String, nullable=False)
    logs = db.relationship("Log")

    def to_json(self):
        return {
            "firstName": self.firstName,
            "lastName": self.lastName,
            "email": self.email
        }

class Log(db.Model):
    __tablename__ = "logs"
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String, nullable=False)
    dateTime = db.Column(db.DateTime, nullable=False)
    analysis = db.Column(db.Float, nullable=False)
    userId = db.Column(db.Integer, db.ForeignKey("users.id"))

    def to_json(self):
        return {
            "content": self.content,
            "dateTime": self.dateTime,
            "analysis": self.analysis
        }