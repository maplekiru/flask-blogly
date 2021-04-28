"""Blogly application."""

from flask import Flask
from models import db, connect_db, User

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

connect_db(app)
db.create_all()

from flask_debugtoolbar import DebugToolbarExtension
app.config['SECRET_KEY'] = "SECRET!"
debug = DebugToolbarExtension(app)


@app.route('/')
def home():
    """ """
    return redirect('/users')

@app.route('/users')
def users():


# GET /
# Redirect to list of users. (We’ll fix this in a later step).
# GET /users
# Show all users.

# Make these links to view the detail page for the user.

# Have a link here to the add-user form.

# GET /users/new
# Show an add form for users
# POST /users/new
# Process the add form, adding a new user and going back to /users
# GET /users/[user-id]
# Show information about the given user.

# Have a button to get to their edit page, and to delete the user.

# GET /users/[user-id]/edit
# Show the edit page for a user.

# Have a cancel button that returns to the detail page for a user, and a save button that updates the user.

# POST /users/[user-id]/edit
# Process the edit form, returning the user to the /users page.
# POST /users/[user-id]/delete
# Delete the user.
