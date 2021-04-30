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

    __table_args__ = (
        db.UniqueConstraint('first_name', 'last_name', 'image_url', name='unique_user'),)

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
    __table_args__ = (
        db.UniqueConstraint('title', 'content', 'user_id', name='unique_post'),)

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
    
    tags = db.relationship(
        'Tag',
        secondary="posttags",
        backref="posts"
        )

    def __repr__(self):
        """Show info about post."""

        p = self
        return f"<Post {p.id} {p.title} by user: {p.user_id}>"

class Tag(db.Model):
    """Tag."""

    __tablename__ = "tags"

    id = db.Column(
        db.Integer,
        primary_key=True,
        autoincrement=True)
    name = db.Column(db.String(20), nullable=False, unique=True)           
    
    def __repr__(self):
        """A tag that describes post(s)."""

        t = self
        return f"<Tag {t.id} {t.name}>"

class PostTag(db.Model):
    """PostTag."""

    __tablename__ = "posttags"

    post_id = db.Column(
        db.Integer,
        db.ForeignKey("posts.id"),
        primary_key=True)   
    tag_id = db.Column(
        db.Integer, 
        db.ForeignKey("tags.id"), 
        primary_key=True)       
    
    @classmethod
    def update_tags(cls, post, tag_list):
        """
        On edit of post tags in edit post form
        update posttags
        """
        old_tags = post.tags
        for tag in old_tags:
            if tag not in tag_list:
                post_tag = PostTag.query.get((post.id,tag.id))
                db.session.delete(post_tag)
                #db.session.commit()
                
        for tag in tag_list:
            if tag not in old_tags:
                assign_tag = PostTag(
                    post_id=post.id,
                    tag_id=int(tag)
                )
                db.session.add(assign_tag)
            
        db.session.commit()

    #post method
    @classmethod
    def delete_posttag_for_post(cls, post):
        """
        deletes the posttag records for a post 
        before deleting the post
        """
        tags = post.tags
        #single line to delete
        #PostTag.query.filter_by(post_id=post.id).delete()
        for tag in tags:
            post_tag = PostTag.query.get((post.id,tag.id))
            db.session.delete(post_tag)
            #db.session.commit()
    
    @classmethod
    def delete_posttag_for_tag(cls, tag):
        """
        deletes the posttag records for a tag 
        before deleting the tag
        """
        posts = tag.posts
        for post in posts:
            post_tag = PostTag.query.get((post.id,tag.id))
            db.session.delete(post_tag)
            #db.session.commit()

    @classmethod
    def assign_tag_to_post(cls,tag_list,post):
        """
        Assign posttag for a new post with tags
        """
        for tag in tag_list:
            assign_tag = PostTag(
                post_id=post.id,
                tag_id=int(tag)
            )
            db.session.add(assign_tag)

    def __repr__(self):
        """Post-tag assignment."""

        pt = self
        return f"<Post Id {pt.post_id} Tag Id{pt.tag_id}>"

