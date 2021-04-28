"""Recipe Model Test"""
from app import app
import os
from unittest import TestCase
from models import db, User, Recipe, FavoriteRecipe


os.environ['DATABASE_URL'] = 'postgresql:///homestew_test'

db.create_all()


class RecipeModelTestCase(TestCase):
    """Test views for recipes"""

    def setUp(self):
        """Create test client, add sample data."""
        db.drop_all()
        db.create_all()

        self.uid = 94566
        u = User.signup("First", "User", "tester", "testing@test.com",
                        "password", None)
        u.id = self.uid

        self.r_id = 9
        r = Recipe.save("Rice and Peas", None, 11,
                        None, 30, 100, "This is the recipe summary")
        r.id = self.r_id
        db.session.commit()

        self.u = User.query.get(self.uid)
        self.r = Recipe.query.get(self.r_id)

        self.client = app.test_client()

    def tearDown(self):
        res = super().tearDown()
        db.session.rollback()
        return res

    def test_recipe_model(self):
        """Does recipe model work?"""

        r = Recipe(title="Rice and Peas", recipe_source_url=None,
                   recipe_source_id=112334,
                   recipe_image=None, likes=30,
                   rating=100, summary="This is the recipe summary")

        r_id = 99
        r.id = r_id

        db.session.add(r)
        db.session.commit()

        u = User.query.get(self.u.id)
        fav = FavoriteRecipe.update_fav(u.id, r_id)

        db.session.add(fav)
        db.session.commit()

        # User should have 1 favorite recipe
        self.assertEqual(len(self.u.favorite_recipes), 1)
        self.assertEqual(self.u.favorite_recipes[0].title, "Rice and Peas")

    def test_save(self):
        r = Recipe.save("Noodles", None, 112334,
                        None, 30, 100, "This is the recipe summary")
        r_id = 999
        r.id = r_id

        db.session.commit()
        r = Recipe.query.get(999)

        self.assertEqual(r.summary, "This is the recipe summary")
        self.assertEqual(r.recipe_source_id, 112334)
        self.assertEqual(r.title, "Noodles")

    def test_delete_recipe(self):
        res = Recipe(title="Rice and Peas", recipe_source_url=None,
                     recipe_source_id=112,
                     recipe_image=None, likes=30,
                     rating=100, summary="This is the recipe summary")

        r_id = 111
        res.id = r_id

        db.session.add(res)
        db.session.commit()

        new_res = Recipe.delete_recipe(112)

        self.assertEqual(new_res, 112)

    def test_get_recipe_index(self):
        res = Recipe.get_recipe_index(self.r.recipe_source_id)

        self.assertNotEqual(res, 9999)
        self.assertNotEqual(res, 9)
