"""Recipe Views Test Case"""

import os
from unittest import TestCase
from models import db, User, Recipe
from app import app, CURR_USER_KEY, API_KEY
RECIPE_ID = 716429


os.environ['DATABASE_URL'] = 'POSTGRESQL:///homestew_test'
app.config['WTF_CSRF_ENABLED'] = False


db.create_all()


class RecipeViewTestCase(TestCase):
    """Test views for recipes"""

    def setUp(self):
        """Create test client, add sample data"""

        db.drop_all()
        db.create_all()

        self.client = app.test_client()

        self.testuser = User.signup("First", "Last",
                                    "Test1", "test@email.com",
                                    "hashed_pwd", None)
        self.testuser_id = 999999
        self.testuser.id = self.testuser_id

        self.testrecipe = Recipe.save("Chicken and Rice", None,
                                      112345, None, 300,
                                      100, "This is the recipe summary")

        db.session.commit()

    def test_save_recipes(self):
        """Can user save recipes"""

        with self.client as c:
            with c.session_transaction() as sess:
                sess[CURR_USER_KEY] = self.testuser.id

            res = c.post(f'/recipes/save/{RECIPE_ID}',
                         data={'apiKey': API_KEY})

            self.assertEqual(res.status_code, 302)
            self.assertEqual(res.location, "http://localhost/")

    def test_remove_recipe(self):
        """Can user remove recipes"""
        with self.client as c:
            with c.session_transaction() as sess:
                sess[CURR_USER_KEY] = self.testuser.id

            res = c.post('/recipes/delete/112345',
                         follow_redirects=True)
            db.session.commit()
            self.assertEqual(res.status_code, 200)

    def test_show_types(self):
        """Can we show categories"""
        with self.client as c:
            with c.session_transaction() as sess:
                sess[CURR_USER_KEY] = self.testuser.id

            res = c.get('/recipes/browse', data={'apiKey': API_KEY})

            self.assertEqual(res.status_code, 200)
