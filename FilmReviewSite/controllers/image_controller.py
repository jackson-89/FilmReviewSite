from flask import Blueprint,request,redirect,abort,url_for,current_app
from pathlib import Path
from models.reviews import Review
import boto3

review_images = Blueprint('review_images',__name__)

@review_images.route("/reviews/<int:id>/image/",methods=["POST"])
def upload_image(id):

    review  = Review.query.get_or_404(id)

    if "image" in request.files:

        image = request.files["image"]

        if Path(image.filename).suffix != ".PNG":
            return abort(400, description="Invalid file type")

        bucket=boto3.resource("s3").Bucket(current_app.config["AWS_S3_BUCKET"])
        bucket.upload_fileobj(image, review.image_filename)

        return redirect(url_for("reviews.get_review", id=id))

    return abort(400, description="No image")