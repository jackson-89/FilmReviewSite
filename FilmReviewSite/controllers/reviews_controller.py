from flask import Blueprint, jsonify,request,render_template,redirect,url_for,current_app
from main import db
from models.reviews import Review
from schemas.reviews_schema import review_schema, reviews_schema
from flask_login  import login_required,current_user
import boto3

reviews = Blueprint('reviews', __name__)

@reviews.route('/')
def home_page():
    data =  {
        "page_title":"Homepage"
    }
    return render_template("homepage.html", page_data=data)


@reviews.route('/reviews/',methods=["GET"])
def get_reviews():
    data = {
        "page_title": "Review Index",
        "reviews": reviews_schema.dump(Review.query.all())
    }
    return render_template("review_index.html", page_data = data)


@reviews.route('/reviews/',methods=["POST"])
def create_review():
    new_review=review_schema.load(request.form)
    db.session.add(new_review)
    db.session.commit()
    return redirect(url_for("reviews.get_reviews"))


@reviews.route('/reviews/<int:id>/',methods=["GET"])
def get_review(id):
    review=Review.query.get_or_404(id)

    s3_client=boto3.client("s3")
    bucket_name=current_app.config["AWS_S3_BUCKET"]
    image_url = s3_client.generate_presigned_url(
        'get_object',
        Params={
            "Bucket":bucket_name,
            "Key": review.image_filename
        },
        ExpiresIn=100
    )
    data = {
        "page_title":"Review Detail",
        "review":review_schema.dump(review),
        "image":image_url
    }
    return render_template("review_detail.html",page_data=data)

#put patch
@reviews.route("/reviews/<int:id>/", methods=["POST"])
def update_review(id):

    review=Review.query.filter_by(review_id=id)

    updated_fields = review_schema.dump(request.form)
    if updated_fields:
        review.update(updated_fields)
        db.session.commit()

    data = {
        "page_title":"Review Detail",
        "review":review_schema.dump(review.first())
    }
    return render_template("review_detail.html",page_data=data)


@reviews.route("/reviews/<int:id>/delete/",methods=["POST"])
def delete_review(id):
    review=Review.query.get_or_404(id)
    db.session.delete(review)
    db.session.commit()
   
    return redirect(url_for("reviews.get_reviews"))

