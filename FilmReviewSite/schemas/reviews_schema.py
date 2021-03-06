from main import ma
from models.reviews import Review
from marshmallow_sqlalchemy import auto_field
from marshmallow.validate import Length

class ReviewsSchema(ma.SQLAlchemyAutoSchema):
    review_id = auto_field(dump_only=True)
    review_name = auto_field(required=True, validate=Length(min=1))
    description = auto_field(validate=Length(min=1))
    creator = ma.Nested(
        "UserSchema",
        only=("id","name","email")
    )
    students=ma.Nested(
        "UserSchema",
        only=("id","name","email")
    ) 

    class Meta:
        model = Review
        load_instance = True

review_schema = ReviewsSchema()
reviews_schema = ReviewsSchema(many=True)
