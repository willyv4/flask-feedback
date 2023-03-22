import imp
from re import U
from turtle import back
import bcrypt
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from sqlalchemy import ForeignKey

db = SQLAlchemy()

bcrypt = Bcrypt()


def connect_db(app):
    """ connect application to database """

    db.app = app
    db.init_app(app)
    app.app_context().push()


class User(db.Model):

    __tablename__ = 'users'

    username = db.Column(db.String(20), nullable=False, primary_key=True)
    password = db.Column(db.Text, nullable=False)
    email = db.Column(db.String(50), nullable=False)
    first_name = db.Column(db.String(30), nullable=False)
    last_name = db.Column(db.String(30), nullable=False)

    feedback = db.relationship(
        "Feedback", backref='User', cascade='all, delete-orphan')

    @classmethod
    def register(cls, username, pwd, email, first, last):

        hashed = bcrypt.generate_password_hash(pwd)
        hashed_utf8 = hashed.decode("utf8")

        return cls(username=username, password=hashed_utf8, email=email, first_name=first, last_name=last)

    @classmethod
    def authenticate(cls, username, pwd):

        u = User.query.filter_by(username=username).first()

        if u and bcrypt.check_password_hash(u.password, pwd):
            return u
        else:
            return False


class Feedback(db.Model):

    __tablename__ = 'feedback'

    id = db.Column(db.Integer, nullable=False, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    username = db.Column(db.Text, db.ForeignKey('users.username'))
