from unittest import TestCase

from app import app
from models import db, User

# Use test database and don't clutter tests with SQL
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly_test'
app.config['SQLALCHEMY_ECHO'] = False

# Make Flask errors be real errors, rather than HTML pages with error info
app.config['TESTING'] = True

# This is a bit of hack, but don't use Flask DebugToolbar
app.config['DEBUG_TB_HOSTS'] = ['dont-show-debug-toolbar']

db.drop_all()
db.create_all()

class BloglyTestCase(TestCase):
    """Tests for views for test Users."""

    def setUp(self):
        """Add sample user."""

        User.query.delete()

        user = User(first_name="John", last_name="Doe", image_url='http://cdn.akc.org/content/article-body-image/golden_puppy_dog_pictures.jpg')
        db.session.add(user)
        db.session.commit()

        self.user_id = user.id

    def tearDown(self):
        """Clean up any fouled transaction."""

        db.session.rollback()

    def test_users(self):
        with app.test_client() as client:
            resp = client.get("/")
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('>Users<', html)
            self.assertIn('John', html)

    def test_add_user(self):
        with app.test_client() as client:
            d = {"first_name": "Jane", "last_name": "Doe", "image_url": ''}
            resp = client.post("/", data=d, follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn("Jane", html)

    # def test_user_profile(self):
    #     with app.test_client() as client:
    #         d = {"name": "TestPet2", "species": "cat", "hunger": 20}
    #         resp = client.post("/", data=d, follow_redirects=True)
    #         html = resp.get_data(as_text=True)

    #         self.assertEqual(resp.status_code, 200)
    #         self.assertIn("<h1>TestPet2</h1>", html)

    # def test_delete_user_profile(self):