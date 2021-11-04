from flask import Blueprint, jsonify,request
from main import db
from models.reviews import Review
from schemas.reviews_schema import review_schema, reviews_schema

reviews = Blueprint('reviews', __name__)

@reviews.route('/reviews/',methods=["GET"])
def review_index():
    reviews = Review.query.all()
    return jsonify(reviews_schema.dump(reviews))

@reviews.route('/reviews/',methods=["POST"])
def create_review():
    new_review=review_index.load(request.json)
    db.session.add(new_review)
    db.session.commit()
    return jsonify(review_schema.dump(new_review))

@reviews.route('/reviews/<int:id>/',methods=["GET"])
def get_review(id):
    review=Review.query.get_or_404(id)
    return jsonify(review_schema.dump(review))

@reviews.route("/reviews/<int:id>/", methods=["PUT","PATCH"])
def update_review(id):
    review=Review.query.filter_by(review_id=id)
    updated_fields = review_schema.dump(request.json)
    if updated_fields:
        review.update(updated_fields)
        db.session.commit()
    return jsonify(review_schema.dump(review.first()))

@reviews.route("/reviews/<int:id>/",methods=["DELETE"])
def delete_review(id):
    review=Review.query.get_or_404(id)
    db.session.delete(review)
    db.session.commit()
    return jsonify(review_schema.dump(review))