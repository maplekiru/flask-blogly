from unittest import TestCase

from app import app
from models import db, User, Post

# Use test database and don't clutter tests with SQL
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly_test'
app.config['SQLALCHEMY_ECHO'] = False

# Make Flask errors be real errors, rather than HTML pages with error info
app.config['TESTING'] = True

# This is a bit of hack, but don't use Flask DebugToolbar
app.config['DEBUG_TB_HOSTS'] = ['dont-show-debug-toolbar']

db.drop_all()
db.create_all()

class UserTestCase(TestCase):
    """Tests for views for test Users."""

    def setUp(self):
        """Add sample user."""

        Post.query.delete()
        User.query.delete()

        user = User(
            first_name="John", 
            last_name="Doe", 
            image_url='http://cdn.akc.org/content/article-body-image/golden_puppy_dog_pictures.jpg')
        db.session.add(user)
        db.session.commit()

        self.user_id = user.id

    def tearDown(self):
        """Clean up any fouled transaction."""

        db.session.rollback()

    def test_users(self):
        with app.test_client() as client:
            resp = client.get("/users")
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('>Users<', html)
            self.assertIn('John', html)

    def test_add_user(self):
        with app.test_client() as client:
            d = {"first_name": "Jane", "last_name": "Doe", "image_url": ''}
            resp = client.post("/users/new", data=d, follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn("Jane", html)

    def test_user_profile(self):
        with app.test_client() as client:
            resp = client.get(f"/users/{self.user_id}")
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn("John", html)
            self.assertIn("Edit", html)

    def test_delete_user_profile(self):
        with app.test_client() as client:
            resp = client.post(f'/users/{self.user_id}/delete', follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertNotIn("John", html)

class PostTestCase(TestCase):
    """Tests for views for test Posts."""

    def setUp(self):
        """Add sample user."""

        Post.query.delete()
        User.query.delete()
        

        user = User(
            first_name="John", 
            last_name="Doe", 
            image_url='http://cdn.akc.org/content/article-body-image/golden_puppy_dog_pictures.jpg')
        
        db.session.add(user)

        db.session.commit()

        self.user_id = user.id

        post = Post(title='testpost1', content='test content1', user_id=self.user_id)

        db.session.add(post)

        db.session.commit()

        self.post_id = post.id     

    def tearDown(self):
        """Clean up any fouled transaction."""

        db.session.rollback()

    def test_post_list(self):
        with app.test_client() as client:
            resp = client.get(f"/users/{self.user_id}")
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('>testpost1<', html)

    def test_add_post(self):
        with app.test_client() as client:
            d = {"title": "testpost2", "content": "test content2", "user_id": self.user_id}
            resp = client.post(f"/users/{self.user_id}/posts/new", data=d, follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn("testpost2", html)

    def test_user_profile(self):
        with app.test_client() as client:
            d = {"title": "testpost edit", "content": "test content edit"}
            resp = client.post(f"/posts/{self.post_id}/edit", data=d, follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn("testpost edit", html)
            self.assertIn("John", html)

    def test_delete_post(self):
        with app.test_client() as client:
            resp = client.post(f'/posts/{self.post_id}/delete', follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertNotIn("testpost1", html)