import os
from flask import Flask,request,jsonify
from flask_sqlalchemy import SQLAlchemy
import psycopg2

(
    db_user,
    db_pass,
    db_name,
    db_domain
) = (os.environ.get(item) for item in [
    "DB_USER",
    "DB_PASS",
    "DB_NAME",
    "DB_DOMAIN"
    ]
)

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = f"postgresql+psycopg2://{db_user}:{db_pass}@{db_domain}/{db_name}"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

class Review(db.Model):
    __tablename__="reviews"
    review_id = db.Column(db.Integer, primary_key=True)
    review_name = db.Column(db.String(80), unique=True, nullable=False)

    def __init__(self, review_name):
        self.review_name = review_name

    @property
    def serialize(self):
        return {
            "review_id": self.review_id,
            "review_name":self.review_name
        }    

db.create_all()

@app.route('/reviews/',methods=["GET"])
def review_index():
    reviews = Review.query.all()
    return jsonify([review.serialize for review in reviews])

@app.route('/reviews/',methods=["POST"])
def create_review():
    new_review=Review(request.json['review_name'])
    db.session.add(new_review)
    db.session.commit()
    return jsonify(new_review.serialize)

@app.route('/reviews/<int:id>/',methods=["GET"])
def get_review(id):
    review=Review.query.get_or_404(id)
    return jsonify([review.serialize])

@app.route("/reviews/<int:id>/", methods=["PUT","PATCH"])
def update_review(id):
    review=Review.query.filter_by(review_id=id)
    review.update(dict(review_name=request.json["review_name"]))
    db.session.commit()
    return jsonify(review.first().serialize)

@app.route("/reviews/<int:id>/",methods=["DELETE"])
def delete_review(id):
    review=Review.query.get_or_404(id)
    db.session.delete(review)
    db.session.commit()
    return jsonify(review.serialize)
    

if __name__ == '__main__':
    app.run(debug=True)