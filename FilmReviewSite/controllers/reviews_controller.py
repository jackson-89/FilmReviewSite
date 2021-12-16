from flask import Blueprint, jsonify,request,render_template,redirect,url_for,current_app,abort
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
        "reviews": reviews_schema.dump(Review.query.order_by(Review.creator_id).all())
    }
    return render_template("review_index.html", page_data = data)


@reviews.route('/reviews/',methods=["POST"])
@login_required
def create_review():
    new_review=review_schema.load(request.form)

    new_review.creator=current_user

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
@login_required
def update_review(id):
    review=Review.query.filter_by(review_id=id)

    if current_user.id != review.first().creator_id:
        abort(403, "You do not have permission to alter this review!")

    updated_fields = review_schema.dump(request.form)
    if updated_fields:
        review.update(updated_fields)
        db.session.commit()

    data = {
        "page_title":"Review Detail",
        "review":review_schema.dump(review.first())
    }
    return render_template("review_detail.html",page_data=data)

@reviews.route("/reviews/<int:id>/enrol/", methods=["POST"])
@login_required
def enrol_in_course(id):
    review=Review.query.get_or_404(id)
    review.students.append(current_user)
    db.session.commit()
    return redirect(url_for('users.user_detail'))

@reviews.route("/reviews/<int:id>/drop/", methods=["POST"])
@login_required
def drop_course(id):
    review=Review.query.get_or_404(id)
    review.students.remove(current_user)
    db.session.commit()
    return redirect(url_for('users.user_detail'))

@reviews.route("/reviews/<int:id>/delete/",methods=["POST"])
@login_required
def delete_review(id):
    review=Review.query.get_or_404(id)

    if current_user.id != review.creator_id:
        abort(403, "You do not have permission to delete this review!")
        
    db.session.delete(review)
    db.session.commit()
   
    return redirect(url_for("reviews.get_reviews"))

