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
    (We'll fix this in a later step).
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

    return redirect(f'/users/{user.id}')

@app.route('/users/<int:userid>')
def user_profile(userid):
    """
    GET /users/[user-id]
    Show information about the given user.

    Have a button to get to their edit page, and to delete the user.
    """

    user = User.query.get_or_404(userid)
    return render_template("user_profile.html", user=user)

@app.route('/users/<int:userid>/edit')
def edit_profile(userid):
    """
    GET /users/[user-id]/edit
    Show the edit page for a user.

    Have a cancel button that returns to the detail page for a user, and a save button that updates the user.
    """

    user = User.query.get_or_404(userid)
    return render_template("edit_user_form.html", user=user)

@app.route('/users/<int:userid>/edit', methods=["POST"])
def update_user_profile(userid):
    """
    POST /users/[user-id]/edit
    Process the edit form, returning the user to the /users page.
    """
    first_name = request.form['first_name']
    last_name = request.form['last_name']
    image_url = request.form['image_url']
    image_url = image_url if image_url else ''

    user = User.query.get(userid)
    user.first_name = first_name
    user.last_name = last_name
    user.image_url = image_url
   
    db.session.commit()

    return redirect("/users")

@app.route('/users/<int:userid>/delete', methods=["POST"])
def delete_user_profile(userid):
    """
    POST /users/[user-id]/delete
    Delete the user.
    """
    user = User.query.get(userid)
    db.session.delete(user)
    db.session.commit()

    return redirect("/users")
