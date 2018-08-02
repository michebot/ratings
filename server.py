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
    # if the new_email is already inside of our database, will return True
    check_email = User.query.filter(User.email==new_email).first()

    # if returns above query returns None (i.e. new email/user not in database)
    if not check_email:
    # if User.new_email
        new_user = User(email=new_email, password=new_password, 
                        age=int(new_age), zipcode=new_zipcode)

        db.session.add(new_user)
        db.session.commit()

        print('\n\n\nUser added!\n\n\n')

        return redirect('/')

    else:
        return redirect("/")

@app.route('/login', methods=['GET'])
def display_login():
    """Collect user login information"""


    return render_template("login_form.html")


@app.route('/login', methods=['POST'])
def validate_login_info():
    """Validate user log in info."""

    email_inputed = request.form.get("email")
    password_inputed = request.form.get("password")

    user = User.query.filter(User.email==email_inputed).first()
    if not user:
        flash('Please create an account!')
        print('\n\n\nUSER NEEDS TO CREATE ACCOUNT\n\n\n')
        return redirect('/login')

    if user.password != password_inputed:
        flash('Incorrect password!')
        print('\n\n\nUSER DID NOT ENTER CORRECT PASSWORD\n\n\n')
        return redirect('/login')

    session['user_id'] = user.user_id
    # import pdb; pdb.set_trace()
    flash('You are now logged in!')
    print('\n\n\nUSER LOGGED IN\n\n\n')
    return redirect('/')

@app.route('/logout', methods=['GET'])
def log_out():
    """Log user out."""

    del session['user_id'] 

    flash('You have been logged out.')
    print('\n\n\nUSER LOGGED OUT\n\n\n')
    return redirect('/')


@app.route('/user_details')
def render_user_details():
    """Display user details"""
    users = User.query.all()
    ratings = Rating.query.all()

    return render_template('/user_info.html', users=users, ratings=ratings)


@app.route('/movie_list')
def render_movie_details():
    """Show movie details"""

    movies = Movie.query.all()

    pass

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
