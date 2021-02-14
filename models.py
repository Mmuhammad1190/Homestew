"""SQLAlchemy models for Homestew"""

from datetime import datetime

from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy

bcrypt = Bcrypt()
db = SQLAlchemy()


class User(db.Model):
    """User in the system"""

    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.Text, nullable=False)
    username = db.Column(db.Text, nullable=False, unique=True)
    image_url = db.Column(db.Text, default="/static/images/default-pic.png")
    password = db.Column(db.Text, nullable=False)
    fav_recipes = db.relationship('FavoriteRecipe')

    def __repr__(self):
        return f"<User #{self.id}: {self.username}, {self.email}>"

    @classmethod
    def update_user(cls, curr_user, form):
        """Update user profile information"""

        curr_user.username = form.username.data
        curr_user.email = form.email.data
        curr_user.image_url = form.image_url.data or User.image_url.default.arg
        db.session.add(curr_user)
        return curr_user

    @classmethod
    def signup(cls, username, email, password, image_url):
        """Sign up user; Hashes password and adds user to system."""
        hashed_pwd = bcrypt.generate_password_hash(password).decode('UTF-8')
        user = User(username=username, email=email,
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


class Recipe(db.Model):
    """Recipes in the database to be saved"""

    __tablename__ = 'recipes'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text, nullable=False, unique=True)
    recipe_source_id = db.Column(db.Integer, nullable=False)
    recipe_image = db.Column(db.Text, default="/static/images/default-pic.png")
    summary = db.Column(db.Text)


class Ingredient(db.Model):
    """Ingredients for the saved recipes"""

    __tablename__ = 'ingredients'

    id = db.Column(db.Integer, primary_key=True)
    recipe_id = db.Column(db.Integer, db.ForeignKey(
        'recipes.id', ondelete="cascade"))
    name = db.Column(db.Text, nullable=False)
    description = db.Column(db.Text, nullable=False)


class Instruction(db.Model):
    """Instructions/steps for cooking each recipe"""

    __tablename__ = 'instructions'

    id = db.Column(db.Integer, primary_key=True)
    recipe_id = db.Column(db.Integer, db.ForeignKey(
        'recipes.id', ondelete='cascade'))
    step_number = db.Column(db.Text, nullable=False)
    step_detail = db.Column(db.Text, nullable=False)


class FavoriteRecipe(db.Model):
    """Recipes saved by user"""

    __tablename__ = 'fav_recipes'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey(
        'users.id', ondelete='cascade'))
    recipe_id = db.Column(db.Integer, db.ForeignKey(
        'recipes.id', ondelete='cascade'))
    timestamp = db.Column(db.DateTime, nullable=False, default=datetime.now())
    user = db.relationship('User')

    @classmethod
    def update_time(cls):
        """Used to update the datetime on each new message"""
        time = datetime.now()
        return time


def connect_db(app):
    """Connect this database to provided Flask app."""

    db.app = app
    db.init_app(app)
