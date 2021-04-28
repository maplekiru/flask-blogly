"""Blogly application."""

from flask import Flask, redirect, render_template, request
from models import db, connect_db, User

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

connect_db(app)
db.create_all()

@app.route('/')
def home():
    """ 
    GET /
    Redirect to list of users. 
    (We’ll fix this in a later step).
    """
    return redirect('/users')

@app.route('/users')
def users():
    """
    GET /users
    Show all users.

    Make these links to view the detail page for the user.

    Have a link here to the add-user form.
    """
    users = User.get_all_users()
    return render_template('users.html',users=users)

@app.route('/users/new')
def add_user_form():
    """
    GET /users/new
    Show an add form for users
    """
    return render_template('add_user_form.html')

@app.route('/users/new', methods=["POST"])
def add_user():
    """
    POST /users/new
    Process the add form, 
    adding a new user and going back to /users
    """
    first_name = request.form['first_name']
    last_name = request.form['last_name']
    image_url = request.form['image_url']
    image_url = image_url if image_url else None

    user = User(first_name=first_name, last_name=last_name, image_url=image_url)
    db.session.add(user)
    db.session.commit()

    return redirect(f"/{user.id}")
