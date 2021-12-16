from main import db
from models.users import User


enrolments=db.Table(
    'enrolments',
    db.Column("user_id",  db.Integer,db.ForeignKey('flasklogin-users.id'),primary_key=True),
    db.Column("review_id",db.Integer,db.ForeignKey("reviews.review_id"), primary_key=True)
)
# Tells the ORM what tables should exist
class Review(db.Model):
        __tablename__="reviews"
        review_id = db.Column(db.Integer, primary_key=True)
        review_name = db.Column(db.String(80), unique=True, nullable=False)
        description=db.Column(db.String(200), server_default="No description provided")

        creator_id = db.Column(db.Integer, db.ForeignKey('flasklogin-users.id'))

        students=db.relationship(
            User,
            secondary=enrolments,
            backref=db.backref("enrolled_courses"),
            lazy="joined"
        )
        @property
        def image_filename(self):
            return f"review_images/{self.review_id}.png"

       