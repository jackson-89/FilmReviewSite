from flask import Flask

app = Flask(__name__)

@app.route('/')
def hello_world():
    return "Hello, world! Check this out!"

@app.route('/users/')
def get_users():
    return "This will be a list of all users that have made reviews"

@app.route('/users/<int:user_id>')
def get_specific_user(user_id):
    return f"This will be a page displaying info about a specific user about user {user_id}"

if __name__ == '__main__':
    app.run(debug=True)