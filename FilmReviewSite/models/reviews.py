from main import db
# Tells the ORM what tables should exist
class Review(db.Model):
        __tablename__="reviews"
        review_id = db.Column(db.Integer, primary_key=True)
        review_name = db.Column(db.String(80), unique=True, nullable=False)
        description=db.Column(db.String(200),default="No description provided")

        @property
        def image_filename(self):
            return f"review_images/{self.review_id}.png"

       