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

    def to_json(self):
        return {
            "firstName": self.firstName,
            "lastName": self.lastName,
        }

class Log(db.Model):
    __tablename__ = "logs"
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String, nullable=False)
    dateTime = db.Column(db.DateTime, nullable=False)
    userId = db.Column(db.Integer, db.ForeignKey("users.id"))
    analysis = db.relationship("Analysis", backref="log")

    def to_json(self):
        return {
            "content": self.content,
            "dateTime": self.dateTime
        }

class Analysis(db.Model):
    __tablename__ = "analyses"
    id = db.Column(db.Integer, primary_key=True)
    result = db.Columnt(db.Float, nullable=False)
    logId = db.Column(db.Integer, db.ForeignKey("logs.id"))

    def to_json(self):
        return {
            "result": self.result
        }