"""Login page for the photo sharing app."""
import flask
from flask import request, redirect, session, make_response
import insta485
from insta485.views.accounts.check_password import check_password


@insta485.app.route('/accounts/login/', methods=['GET', 'POST'])
def show_login():
    """Display /accounts/login."""
    if request.method == 'POST':
        return do_the_login()
    else:
        return show_the_login_form()


def do_the_login():
    """Handle the login process."""
    username = flask.request.authorization['username']
    password = flask.request.authorization['password']
    print(username, password)

    connection = insta485.model.get_db()

    cur = connection.execute(
        "SELECT * FROM users WHERE username = ?",
        (username,)
    )
    user = cur.fetchone()

    if (user == None) or check_password(user['password'], password):
        print("Invalid username or password.")
        return flask.render_template("login.html", error="Invalid username or password."), 403

    # Successful login, set the user ID in the session
    session['username'] = user['username']
    response = make_response("Login successful!", 200)
    response.set_cookie('username', user['username'])

    print(flask.session['username'])

    # Redirect to the desired page after successful login
    target = request.args.get('target')
    return redirect(target or '/')



def show_the_login_form():
    """Display /accounts/login form."""
    return flask.render_template("login.html")


@insta485.app.route('/accounts/logout/', methods=['GET', 'POST'])
def do_logout():
    """Logout the user."""
    # Remove the username from the session if it's there
    flask.session.clear()
    session['username'] = None
    response = make_response("Logout successful!", 200)
    response.set_cookie('username', '')

    return redirect('/accounts/login/')
