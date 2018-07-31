"""Movie Ratings."""

from jinja2 import StrictUndefined

from flask import (Flask, render_template, redirect, request, flash, session)
from flask_debugtoolbar import DebugToolbarExtension

from model import User, Rating, Movie, connect_to_db, db


app = Flask(__name__)

# Required to use Flask sessions and the debug toolbar
app.secret_key = "ABC"

# Normally, if you use an undefined variable in Jinja2, it fails
# silently. This is horrible. Fix this so that, instead, it raises an
# error.
app.jinja_env.undefined = StrictUndefined


@app.route('/')
def index():
    """Homepage."""
    return render_template("homepage.html")
    # return "<html><body>Placeholder for the homepage.</body></html>"


@app.route('/users')
def user_list():
    """Show list of users"""

    users = User.query.all()
    return render_template("user_list.html", users=users)

@app.route('/register', methods=["GET"])
def register_form():
    """Obtain user information"""

    return render_template("register_form.html")

@app.route('/register', methods=["POST"])
def register_process():
    """Save user information"""
    new_email = request.form.get("email")
    new_password = request.form.get("password")
    new_age = request.form.get("age")
    new_zipcode = request.form.get("zipcode")

    if User.query.filter(User.email==new_email) is not None:
    # if User.new_email
        return redirect("/")

    else:
        new_user = User(email=new_email, password=new_password, age=new_age, zipcode=new_zipcode)

        db.session.add(new_user)
        db.session.commit()


if __name__ == "__main__":
    # We have to set debug=True here, since it has to be True at the
    # point that we invoke the DebugToolbarExtension
    app.debug = True
    # make sure templates, etc. are not cached in debug mode
    app.jinja_env.auto_reload = app.debug

    connect_to_db(app)

    # Use the DebugToolbar
    DebugToolbarExtension(app)

    DEBUG_TB_INTERCEPT_REDIRECTS=False

    app.run(port=5000, host='0.0.0.0')
