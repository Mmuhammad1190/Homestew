"""SQLAlchemy models for Homestew"""

from datetime import datetime

from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy

bcrypt = Bcrypt()
db = SQLAlchemy()


def connect_db(app):
    """Connect this database to provided Flask app."""

    db.app = app
    db.init_app(app)


class User(db.Model):
    """User in the system"""

    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.Text, nullable=False)
    first_name = db.Column(db.Text, nullable=False)
    last_name = db.Column(db.Text, nullable=False)
    username = db.Column(db.Text, nullable=False, unique=True)
    image_url = db.Column(db.Text, default="/static/images/default-pic.png")
    password = db.Column(db.Text, nullable=False)
    favorite_recipes = db.relationship(
        'Recipe', backref='user', secondary='fav_recipes')

    def __repr__(self):
        return f"<User #{self.id}: {self.username}, {self.email}>"

    @classmethod
    def update_user(cls, curr_user, form):
        """Update user profile information"""
        curr_user.first_name = form.first_name.data
        curr_user.last_name = form.last_name.data
        curr_user.username = form.username.data
        curr_user.email = form.email.data
        curr_user.image_url = form.image_url.data or User.image_url.default.arg
        db.session.add(curr_user)
        return curr_user

    @classmethod
    def signup(cls, first_name, last_name, username, email, password,
               image_url):
        """Sign up user; Hashes password and adds user to system."""
        hashed_pwd = bcrypt.generate_password_hash(password).decode('UTF-8')
        user = User(first_name=first_name, last_name=last_name,
                    username=username, email=email,
                    password=hashed_pwd, image_url=image_url)
        db.session.add(user)
        return user

    @classmethod
    def authenticate(cls, username, password):
        """Find user with `username` and `password`.
        If can't find matching user (or if password is wrong), returns False.
        """
        user = cls.query.filter_by(username=username).first()

        if user:
            is_auth = bcrypt.check_password_hash(user.password, password)
            if is_auth:
                return user

        return False

    @classmethod
    def get_user_fav_recipes(cls, user_id):
        """Fetch all user favorite recipes"""
        user = User.query.get(user_id)

        return user.favorite_recipes

    @classmethod
    def remove_user(cls, user_id):
        """Remove current user account"""
        user = User.query.get(user_id)

        db.session.delete(user)
        return user


class Recipe(db.Model):
    """Recipes in the database to be saved"""

    __tablename__ = 'recipes'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.Text, nullable=False)
    recipe_source_url = db.Column(db.Text, nullable=True)
    recipe_source_id = db.Column(db.Integer, nullable=False, unique=True)
    recipe_image = db.Column(db.Text, default="/static/images/default-pic.png")
    likes = db.Column(db.Integer, nullable=True, default=0)
    rating = db.Column(db.Integer, nullable=True, default=100)
    summary = db.Column(db.Text)

    @classmethod
    def save(cls, title, recipe_source_url, recipe_source_id, recipe_image,
             likes, rating, summary):
        """Save individual recipe to database"""

        recipe = Recipe(title=title, recipe_source_url=recipe_source_url,
                        recipe_source_id=recipe_source_id,
                        recipe_image=recipe_image, likes=likes,
                        rating=rating, summary=summary)
        db.session.add(recipe)
        return recipe

    @classmethod
    def delete_recipe(cls, recipe_source_id):
        """Delete user saved recipe from database"""

        recipe = Recipe.query.filter(
            Recipe.recipe_source_id == recipe_source_id).first()

        db.session.delete(recipe)

        return recipe_source_id

    @classmethod
    def get_recipe_index(cls, recipe_source_id):
        """Get the primary key index of a saved recipe in database"""

        index = db.session.query(Recipe.id).filter(
            Recipe.recipe_source_id == recipe_source_id)
        return index


class FavoriteRecipe(db.Model):
    """Recipes saved by user"""

    __tablename__ = 'fav_recipes'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey(
        'users.id', ondelete='cascade'))
    recipe_id = db.Column(db.Integer, db.ForeignKey(
        'recipes.id', ondelete='cascade'))
    timestamp = db.Column(db.DateTime, nullable=False, default=datetime.now())

    db.relationship('users')

    @classmethod
    def update_fav(cls, user_id, recipe_id):
        """Used to save a favorite recipe to database"""

        fav_recipe = FavoriteRecipe(user_id=user_id, recipe_id=recipe_id)
        db.session.add(fav_recipe)
        return fav_recipe
