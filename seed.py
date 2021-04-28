from models import User, db
from app import app

# Create all tables
db.drop_all()
db.create_all()

# If table isn't empty, empty it
User.query.delete()

# Add pets
user_momo = User(first_name='Momo', last_name="Enokida")
user_kiru = User(first_name='Kiru', last_name="R", image_url='http://cdn.akc.org/content/article-body-image/golden_puppy_dog_pictures.jpg')


# Add new objects to session, so they'll persist
db.session.add(user_momo)
db.session.add(user_kiru)

# Commit--otherwise, this never gets saved!
db.session.commit()
