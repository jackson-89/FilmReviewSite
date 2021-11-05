from main import db
from flask import Blueprint

db_commands = Blueprint("db", __name__)

@db_commands.cli.command("create")
def create_db():
    """Creates tables in the database based on the models."""
    db.create_all()
    print("Tables Created!")

@db_commands.cli.command("drop")
def drop_db():
    """Drops all the tables in the database."""
    db.drop_all()
    print("Tables deleted!")

@db_commands.cli.command("seed")
def seed_db():
    from models.reviews import Review
    from faker import Faker
    faker = Faker()

    for i in range(20):
        review = Review(faker.catch_phrase())
        db.session.add(review)
        
    db.session.commit()
    print("Tables seeded!")

@db_commands.cli.command("reset")
def reset_db():
    """Drops, creates and seeds tables in one step"""
    db.drop_all()
    print("Tables deleted!")
    db.create_all()
    print("Tables Created!")
    from models.reviews import Review
    from faker import Faker
    faker = Faker()

    for i in range(20):
        review = Review(faker.catch_phrase())
        db.session.add(review)
        
    db.session.commit()
    print("Tables seeded!")