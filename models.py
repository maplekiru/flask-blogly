"""Models for Blogly."""
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, DateTime
import datetime

db = SQLAlchemy()


def connect_db(app):
    """Connect to database."""

    db.app = app
    db.init_app(app)

class User(db.Model):
    """User."""

    __tablename__ = "users"

    id = db.Column(db.Integer,
                   primary_key=True,
                   autoincrement=True)
    first_name = db.Column(db.String(50),
                    nullable=False)               
    last_name = db.Column(db.String(50),
                    nullable=False)
    image_url = db.Column(db.String(), nullable=False, default='')
    
    #ask about creating uniqueness for full profile? (Add constraint)

    posts = db.relationship('Post',backref='user')

    def __repr__(self):
        """Show info about user."""

        u = self
        return f"<User {u.id} {u.first_name} {u.last_name}>"
    


class Post(db.Model):
    """Post."""

    __tablename__ = "posts"

    id = db.Column(
        db.Integer,
        primary_key=True,
        autoincrement=True)
    title = db.Column(db.String(50), nullable=False)               
    content = db.Column(db.Text(),nullable=False)
    created_at = db.Column(
        DateTime(timezone=True), 
        default=datetime.datetime.utcnow, 
        nullable=False)
    user_id = db.Column(
        db.Integer, 
        db.ForeignKey("users.id"), 
        nullable=False)
    

    def __repr__(self):
        """Show info about post."""

        p = self
        return f"<Post {p.id} {p.title} by user: {p.user_id}>"
