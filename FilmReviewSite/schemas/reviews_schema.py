from main import ma
from models.reviews import Review
from marshmallow_sqlalchemy import auto_field

class ReviewsSchema(ma.SQLAlchemyAutoSchema):
    review_id = auto_field(dump_only=True)

    class Meta:
        model = Review
        load_instance = True

review_schema = ReviewsSchema()
reviews_schema = ReviewsSchema(many=True)
