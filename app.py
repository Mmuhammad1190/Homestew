"""Homestew Recipe App"""
import requests
import json
from flask import Flask, render_template, flash, redirect, session, g
from flask_debugtoolbar import DebugToolbarExtension
from sqlalchemy.exc import IntegrityError
from secrets import SECRET, os, API_KEY


from models import db, connect_db, User, Recipe, FavoriteRecipe
from forms import SelectForm, UserAddForm, LoginForm, DeleteAccountForm


app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = (
    os.environ.get('DATABASE_URI', 'postgres:///homestew'))

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
app.config['SECRET_KEY'] = SECRET
app.config['WTF_CSRF_ENABLED'] = False
debug = DebugToolbarExtension(app)

connect_db(app)

CURR_USER_KEY = "curr_user"
BASE_URL = 'https://api.spoonacular.com/recipes'

######################################################################
# User signup/login/logout


@app.before_request
def add_user_to_g():
    """If user logged in, add curr user to Flask global"""

    if CURR_USER_KEY in session:
        g.user = User.query.get(session[CURR_USER_KEY])
    else:
        g.user = None


def do_login(user):
    """Log in user"""

    session[CURR_USER_KEY] = user.id


def do_logout():
    """Logout user"""

    if CURR_USER_KEY in session:
        del session[CURR_USER_KEY]


@app.route('/signup', methods=["GET", "POST"])
def signup():
    """Handle user signup.

    Create new user and add to DB. Redirect to home page.

    If form not valid, present form.

    If the there already is a user with that username: flash message
    and re-present form.
    """

    form = UserAddForm()

    if form.validate_on_submit():
        try:
            user = User.signup(
                first_name=form.first_name.data,
                last_name=form.last_name.data,
                username=form.username.data,
                password=form.password.data,
                email=form.email.data,
                image_url=form.image_url.data or User.image_url.default.arg,
            )
            db.session.commit()

        except IntegrityError:
            flash("Username already taken", 'danger')
            return render_template('users/signup.html', form=form)

        do_login(user)
        flash(f"Hello, {user.username}!", "success")
        return redirect("/")

    else:
        return render_template('users/signup.html', form=form)


@app.route('/login', methods=["GET", "POST"])
def login():
    """Handle user login."""

    form = LoginForm()

    if form.validate_on_submit():
        user = User.authenticate(form.username.data,
                                 form.password.data)

        if user:
            do_login(user)
            flash(f"Welcome back, {user.first_name}!", "success")
            return redirect("/")

        flash("Invalid Username/Password! Please Try Again!", 'danger')

    return render_template('users/login.html', form=form)


@app.route('/logout')
def logout():
    """Handle logout of user."""

    do_logout()
    flash("You have logged out, See you soon!", "success")
    return redirect('/')


####################################################
# Users Search routes

@app.route('/search', methods=["GET", "POST"])
def search_page():
    """Search and return for recipes using form queries

    If 'GET' returns search form and random recipes

    If 'POST' returns api request data as JSON
    *certain key names are changed to match the parameters in API*
    """

    form = SelectForm()

    params = {"apiKey": API_KEY, "number": 100}

    if form.validate_on_submit():
        for k, v in form.data.items():
            if (v != 'None'):
                params[k] = v

        for key in params:
            if (key == 'exclude_cuisine'):
                params['excludeCuisine'] = params.pop('exclude_cuisine')
            elif (key == 'meal_type'):
                params['type'] = params.pop('meal_type')
        print(params)
        res = requests.get(f"{BASE_URL}/complexSearch", params)
        return res.json()
    else:
        return render_template('/recipes/search.html', form=form)


@app.route('/search/recipes/<int:recipe_id>', methods=['POST', 'GET'])
def show_recipe(recipe_id):
    """Show individual recipe from search query"""
    if not g.user:
        flash('Access Unauthorized! Please login to view/save recipes!', "danger")
        return redirect('/')

    params = {"apiKey": API_KEY}

    res = requests.get(f"{BASE_URL}/{recipe_id}/information", params)
    widget = requests.get(
        f"{BASE_URL}/{recipe_id}/nutritionWidget.json", params)

    recipe = json.loads(res.content)
    nutrition = json.loads(widget.content)
    return render_template('/recipes/recipe.html', nutrition=nutrition, recipe=recipe)

##########################################################
# User Home/Profile/Delete/Favorites Routes


@app.route('/')
def home():
    """If user added to session, show user homepage. If no user,
    show anonymous homepage"""
    if g.user:
        return render_template('home.html')
    else:
        return render_template('home_anon.html')
    return render_template('home_anon.html')


@app.route('/users/<int:user_id>', methods=['GET', 'POST'])
def show_profile(user_id):
    """Show individual user profile"""

    if not g.user:
        flash("Access unauthorized. Please login to view profile!", "danger")
        return redirect("/")

    user = User.query.get_or_404(user_id)
    saved_recipes = User.get_user_fav_recipes(user_id)
    form = UserAddForm()
    delete_form = DeleteAccountForm()

    if form.validate_on_submit():
        User.update_user(user, form)
        db.session.commit()

        return redirect(f'/users/{user_id}')

    if delete_form.validate_on_submit():
        valid = User.authenticate(user.username, delete_form.password.data)

        if (valid):
            User.remove_user(user_id)
            db.session.commit()

            do_logout()
        return redirect("/")
    return render_template('/users/profile.html', saved_recipes=saved_recipes, user=user, form=form, delete_form=delete_form)


@app.route('/users/<int:user_id>/favorites')
def show_favorites(user_id):
    """Show user favorite recipes"""

    if not g.user:
        flash("Access unauthorized. Please login to view profile!", "danger")
        return redirect("/")

    saved_recipes = User.get_user_fav_recipes(user_id)
    user = User.query.get_or_404(user_id)
    return render_template('/users/favorites.html', saved_recipes=saved_recipes, user=user)
###########################################################
# Recipes Routes


@app.route('/recipes/save/<int:recipe_id>')
def save_recipe(recipe_id):
    """Save individual recipe"""

    params = {"apiKey": API_KEY}

    res = requests.get(f"{BASE_URL}/{recipe_id}/information", params)
    recipe = json.loads(res.content)

    Recipe.save(recipe['title'], recipe['spoonacularSourceUrl'], recipe['id'],
                recipe['image'], recipe['aggregateLikes'], recipe['spoonacularScore'],
                recipe['summary'])
    db.session.commit()

    saved_recipe_index = Recipe.get_recipe_index(recipe_id)

    FavoriteRecipe.update_fav(g.user.id, saved_recipe_index)

    db.session.commit()
    return redirect('/')


@app.route('/recipes/delete/<int:recipe_id>', methods=['POST'])
def remove_recipe(recipe_id):
    """Remove individual recipe from saved recipes"""

    Recipe.delete_recipe(recipe_id)
    db.session.commit()
    flash('Your recipe was removed!', category='success')
    return redirect(f'/users/{g.user.id}')


@app.route('/recipes/browse')
def show_types():
    """Show Browse categories based on cuisine type"""

    if not g.user:
        flash('Please login to browse recipes', "danger")
        return redirect('/')

    params = {"apiKey": API_KEY, "number": 10}

    res = requests.get(f"{BASE_URL}/random", params)
    recipes = json.loads(res.content)
    return render_template('/recipes/browse.html', recipes=recipes)


@app.route('/recipes/browse/<string:recipe_type>')
def browse_types(recipe_type):
    """Browse recipes based on cuisine type"""

    if not g.user:
        flash('Please login to browse recipes', "danger")
        return redirect('/')

    if (recipe_type == 'main_course' or recipe_type == 'side_dish'):
        recipe_type = recipe_type.replace("_", " ")

    params = {"apiKey": API_KEY, "tags": recipe_type, "number": 20}

    res = requests.get(f"{BASE_URL}/random", params)
    recipes = json.loads(res.content)
    recipe_type = recipe_type.title()
    return render_template('/recipes/browse.html', recipes=recipes, recipe_type=recipe_type)


@app.route('/recipes/diets')
def show_diets():
    """Show recipe categories/diets"""

    return render_template("recipes/diets.html")


@app.after_request
def add_header(req):
    """Add non-caching headers on every request."""

    req.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    req.headers["Pragma"] = "no-cache"
    req.headers["Expires"] = "0"
    req.headers['Cache-Control'] = 'public, max-age=0'
    return req
