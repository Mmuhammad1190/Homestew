"""Homestew forms"""

from parameters import CUISINES, DIETS, EXCLUDED_CUISINES, INTOLERANCES, SORT, TYPES
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SelectField, IntegerField
from wtforms.validators import DataRequired, Email, Length
from wtforms.fields.html5 import EmailField, URLField


class UserAddForm(FlaskForm):
    """Form for adding users."""
    first_name = StringField('First Name', validators=[DataRequired()])
    last_name = StringField('Last Name', validators=[DataRequired()])
    username = StringField('Username', validators=[DataRequired()])
    email = EmailField(
        'E-mail', validators=[DataRequired(), Email()])
    image_url = URLField('(Optional) Image URL')
    password = PasswordField('Password', validators=[
                             DataRequired(), Length(min=6)])


class LoginForm(FlaskForm):
    """Login form."""

    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[Length(min=6)])


class DeleteAccountForm(FlaskForm):
    """Form to check password before account deactivation"""

    password = PasswordField('Password', validators=[Length(min=6)])


class SelectForm(FlaskForm):
    """Form for select"""
    query = StringField('What are you in the mood for?')
    diet = SelectField('diet', choices=DIETS)
    cuisine = SelectField('cuisine', choices=CUISINES)
    exclude_cuisine = SelectField('exclude_cuisine', choices=EXCLUDED_CUISINES)
    meal_type = SelectField('type', choices=TYPES)
    intolerance = SelectField('intolerace', choices=INTOLERANCES)
    sort = SelectField('sort', choices=SORT)
    offset = IntegerField('offset', default=0)
