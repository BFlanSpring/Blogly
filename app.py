"""Blogly application."""

from flask import Flask, request, render_template, redirect, flash, session, url_for
from models import db, User

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = 'your-secret-key'


db.init_app(app)
# connect_db(app)
# app = Flask(__name__, static_folder='static')

with app.app_context():
    db.create_all()


@app.route("/", methods=["GET"])
def redirect_to_list():
    """Redirect to list of users"""
    return redirect("/users")
    

@app.route("/users", methods=["GET"])
def show_user_list():
    """Show all users. Make these links to view the detail page for the user. Have a link here to the add-user form"""
    users = User.query.all()
    return render_template("user_list.html", users=users)



@app.route("/users/new", methods=["GET"])
def show_add_form():
    """Show an add form for users"""
    users  = User.query.all()
    return render_template("new_user_form.html", users=users)


@app.route("/users/new", methods=["POST"])
def process_add_form():
    """Process the add form, adding a new user and going back to /users"""

    first_name = request.form['first-name']
    last_name = request.form['last-name']
    profile_pic = request.form['image-link']

    user = User(first_name=first_name, last_name=last_name, profile_pic=profile_pic)
    db.session.add(user)
    db.session.commit()

    return redirect("/users")  # Corrected the redirect URL


@app.route("/users/<int:user_id>", methods=["GET"])
def user_info(user_id):
    """Show information about the given user. Have a button to get to their edit page, and to delete the user."""
    user = User.query.get_or_404(user_id)
    return render_template("user.html", user=user)


@app.route("/users/<int:user_id>/edit", methods=["GET"])
def show_edit_page(user_id):
    """ Show the edit page for a user. Have a cancel button that returns to the detail page for a user, and a save button that updates the user."""
    user = User.query.get_or_404(user_id)
    return render_template("edit_user_form.html", user=user, user_id=user_id)


@app.route("/users/<int:user_id>/edit", methods=["POST"])
def process_edit_form(user_id):
    """Process the edit form, returning the user to the/users page"""
    user = User.query.get_or_404(user_id)

    user.first_name = request.form['first-name']
    user.last_name = request.form['last-name']
    user.profile_pic = request.form['image-link']
    
    
    db.session.commit()

    return redirect(url_for('user_info', user_id=user_id))


@app.route("/users/<int:user_id>/delete", methods = ["POST"])
def delete_user(user_id):
    """Delete the user"""
    user = User.query.get_or_404(user_id)

    db.session.delete(user)
    db.session.commit()

    return redirect("/users")

