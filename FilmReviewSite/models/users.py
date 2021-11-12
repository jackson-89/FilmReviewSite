from main import db
from flask_login import UserMixin
from werkzeug.security import generate_password_hash,check_password_hash

class User(UserMixin, db.Model):
    __tablename__="flasklogin_users"
    id = db.Column(
        db.Integer,
        primary_key=True
    )
    name = db.Column(
        db.String(100),
        nullable=False
    )
    email=db.Column(
        db.String(40),
        unique=True,
        nullable=False
    )
    password=db.Column(
        db.String(200),
        nullable=False
    )

    def check_password(self, password):
        return check_password_hash(self.password, password)