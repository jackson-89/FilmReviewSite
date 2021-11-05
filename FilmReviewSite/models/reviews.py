from main import db
# Tells the ORM what tables should exist
class Review(db.Model):
        __tablename__="reviews"
        review_id = db.Column(db.Integer, primary_key=True)
        review_name = db.Column(db.String(80), unique=True, nullable=False)

        def __init__(self, review_name):
            self.review_name = review_name

       