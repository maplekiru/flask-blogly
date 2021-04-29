"""Blogly application."""

from flask import Flask, redirect, render_template, request, flash, session
from models import db, connect_db, User, Post

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

app.config["SECRET_KEY"] = "$$$"

connect_db(app)

@app.route('/')
def home():
    """ 
    Redirects to users route
    """
    
    return redirect('/users')

@app.route('/users')
def list_users():
    """
    Make a list of users with links to their profiles.

    Have a link here to the add-user form.
    """
    users = User.query.all()
    return render_template('users.html',users=users)

@app.route('/users/new')
def add_user_form():
    """
    Show an add form for users
    """
    return render_template('user_add_form.html')

@app.route('/users/new', methods=["POST"])
def add_user():
    """
    Process the add form, 
    adding a new user to database and redirects to /users
    """
    first_name = request.form['first_name']
    last_name = request.form['last_name']
    image_url = request.form['image_url']
    image_url = image_url if image_url else None

    user = User(
        first_name=first_name, 
        last_name=last_name, 
        image_url=image_url)
    db.session.add(user)
    db.session.commit()

    flash("<p class= 'alert alert-success'> User Added! </p>")
    return redirect(f'/users/{user.id}')

@app.route('/users/<int:user_id>')
def user_profile(user_id):
    """
    Show information about the given user.

    Have a button to get to their edit page, and to delete the user.
    """

    user = User.query.get_or_404(user_id)
    posts = user.posts
    return render_template("user_profile.html", user=user, posts=posts)

@app.route('/users/<int:user_id>/edit')
def edit_profile(user_id):
    """
    Show the edit page for a user.

    Have a cancel button that returns to the detail page for a user, and a save button that updates the user in the database.
    """

    user = User.query.get_or_404(user_id)
    return render_template("user_edit_form.html", user=user)

@app.route('/users/<int:user_id>/edit', methods=["POST"])
def update_user_profile(user_id):
    """
    Process the edit form, redirecting the user to the /users route.
    """
    first_name = request.form['first_name']
    last_name = request.form['last_name']
    image_url = request.form['image_url']
    image_url = image_url if image_url else ''

    user = User.query.get(user_id)
    user.first_name = first_name
    user.last_name = last_name
    user.image_url = image_url
   
    db.session.commit()

    flash("<p class= 'alert alert-success'> User Edited! </p>")

    return redirect("/users")

@app.route('/users/<int:user_id>/delete', methods=["POST"])
def delete_user_profile(user_id):
    """
    Delete the user from the database.
    """
    user = User.query.get(user_id)

    Post.query.filter_by(user_id = user_id).delete()

    for post in user.posts:
        db.session.delete(post)

    db.session.delete(user)
    db.session.commit()

    flash("<p class= 'alert alert-danger'> User Deleted! </p>")

    return redirect("/users")

@app.route('/users/<int:user_id>/posts/new')
def new_post_form(user_id):
    """
    Show form to add a post for that user.
    """
    user = User.query.get(user_id)
    return render_template('post_add_form.html',user=user)

@app.route('/users/<int:user_id>/posts/new', methods = ['POST'])
def add_post(user_id):
    """
    Handle add form; add post and redirect to the user detail page.
    """

    title = request.form['title']
    content = request.form['content']

    post = Post(
        title=title, 
        content=content, 
        user_id=user_id)

    db.session.add(post)
    db.session.commit()

    flash("<p class= 'alert alert-success'> Post added! </p>")

    return redirect(f'/users/{user_id}')

@app.route('/posts/<int:post_id>/')
def post_page(post_id):
    """
    Show information about the given post.

    Have a button to get to their edit page, and to delete the post.
    """

    post = Post.query.get_or_404(post_id)
    user = post.user
    return render_template("post_page.html", 
        post=post,
        user=user)


@app.route('/posts/<int:post_id>/edit')
def edit_post(post_id):
    """
    Show the edit page for a post.

    Have a cancel button that returns to the detail page for a user, and a save button that updates the post in the database.
    """

    post = Post.query.get_or_404(post_id)
    return render_template("post_edit_form.html", 
        post=post)

@app.route('/posts/<int:post_id>/edit', methods=["POST"])
def update_post(post_id):
    """
    Handle editing of a post. Redirect back to the post view.
    """
    title = request.form['title']
    content = request.form['content']

    post = Post.query.get(post_id)
    post.title = title
    post.content = content
   
    db.session.commit()

    flash("<p class= 'alert alert-success'> post Edited! </p>")
    return redirect(f"/posts/{post_id}")

@app.route('/posts/<int:post_id>/delete', methods=["POST"])
def delete_post(post_id):
    """
    Delete the user from the database.
    """
    post = Post.query.get(post_id)
    db.session.delete(post)
    db.session.commit()

    flash("<p class= 'alert alert-danger'> User Deleted! </p>")
    return redirect("/users")
# POST /posts/[post-id]/delete
# Delete the post.