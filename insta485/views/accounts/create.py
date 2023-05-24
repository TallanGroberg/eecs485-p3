"""Create a new account."""
import flask
from flask import request, redirect, session
import insta485
from insta485.views.accounts.check_password import hash_password
from insta485.views.post import handle_file

@insta485.app.route('/accounts/create/', methods=['GET', 'POST'])
def show_create():
    """Display /accounts/create."""
    if request.method == 'POST':
        return do_create()
    else:
        return show_the_create_form()


def do_create():
    """Create a new account."""
    if flask.session['username'] != None:
        return flask.redirect("/accounts/edit/")

    filename = handle_file(flask.request.files['file'])
    username = request.form.get('username')
    password = request.form.get('password')
    password = hash_password(password)
    fullname = request.form.get('fullname')
    email = request.form.get('email')

    connection = insta485.model.get_db()

    connection.execute(
        "INSERT INTO users  (username, password, fullname, email, filename) "
        "VALUES (?, ?, ?, ?, ?)",
        (username, password, fullname, email, filename)
    )
    
    connection.commit()


    session['username'] = username

    return redirect('/')


def show_the_create_form():
    """Display /accounts/create form."""
    return flask.render_template("create.html")
