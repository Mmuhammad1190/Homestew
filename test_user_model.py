"""User model tests."""

from app import app
import os
from unittest import TestCase
from sqlalchemy import exc

from models import db, User

os.environ['DATABASE_URL'] = "postgresql:///homestew_test"


db.create_all()


class UserModelTestCase(TestCase):
    """Test views for users"""

    def setUp(self):
        """Create test client, add sample data."""
        db.drop_all()
        db.create_all()

        u1 = User.signup("First", "User", "test1",
                         "email@email.com", "hashed_pwd", None)
        uid1 = 1111
        u1.id = uid1

        u2 = User.signup("Second", "User", "test2",
                         "email2@email.com", "hashed_pwd2", None)
        uid2 = 2222
        u2.id = uid2

        db.session.commit()

        u1 = User.query.get(uid1)
        u2 = User.query.get(uid2)

        self.u1 = u1
        self.uid1 = uid1

        self.u2 = u2
        self.uid2 = uid2

        self.client = app.test_client()

    def tearDown(self):
        res = super().tearDown()
        db.session.rollback()
        return res

    def test_user_model(self):
        """Does basic user model work correctly?"""

        u = User(email="test@test.com", first_name="Marcellus",
                 last_name="Muhammad",
                 username="MMuhammad", image_url=None,
                 password="HASHED_PASSWORD")

        db.session.add(u)
        db.session.commit()

        # User should have no favorite recipes
        self.assertEqual(len(u.favorite_recipes), 0)

#########
#
# User sign-up tests
#
########
    def test_valid_signup(self):
        u_test = User.signup("First", "User", "user1",
                             "Newemail@email.com", "hashed_pwd", None)
        uid = 999
        u_test.id = uid
        db.session.commit()

        u_test = User.query.get(uid)
        self.assertIsNotNone(u_test)
        self.assertEqual(u_test.first_name, "First")
        self.assertEqual(u_test.last_name, "User")
        self.assertEqual(u_test.username, "user1")
        self.assertEqual(u_test.email, "Newemail@email.com")
        self.assertNotEqual(u_test.password, "hashed_pwd")
        # Bcrypt strings start with $2b$
        self.assertTrue(u_test.password.startswith, "$2b$")
        self.assertEqual(u_test.image_url,
                         "/static/images/default-pic.png")

    def test_invalid_first_name_signup(self):
        invalid = User.signup(
            "", "User", None, "test@test.com", "password", None)
        uid = 999
        invalid.id = uid
        with self.assertRaises(exc.IntegrityError) as context:
            db.session.commit()

    def test_invalid_last_name_signup(self):
        invalid = User.signup(
            "First", "", None, "test@test.com", "password", None)
        uid = 999
        invalid.id = uid
        with self.assertRaises(exc.IntegrityError) as context:
            db.session.commit()

    def test_invalid_username_signup(self):
        invalid = User.signup("First", "User", None,
                              "test@test.com", "password", None)
        uid = 999
        invalid.id = uid
        with self.assertRaises(exc.IntegrityError) as context:
            db.session.commit()

    def test_invalid_email_signup(self):
        invalid = User.signup("First", "User", "user1", None, "password", None)
        uid = 999
        invalid.id = uid
        with self.assertRaises(exc.IntegrityError) as context:
            db.session.commit()

    def test_invalid_password_signup(self):
        with self.assertRaises(ValueError) as context:
            User.signup("First", "User", "user1", "test@test.com", "", None)

        with self.assertRaises(ValueError) as context:
            User.signup("Second", "User", "user2", "test@test.com", None, None)

#########
#
# Authentication tests
#
########

    def test_valid_authentication(self):
        u = User.authenticate(self.u1.username, "hashed_pwd")
        self.assertIsNotNone(u)
        self.assertEqual(u.id, self.uid1)

    def test_invalid_username(self):
        self.assertFalse(User.authenticate("badusername", "password"))

    def test_wrong_password(self):
        self.assertFalse(User.authenticate(self.u1.username, "badpassword"))

    def test_remove_user(self):
        u = User.remove_user(self.u2.id)
        self.assertEqual(u.id, self.u2.id)
