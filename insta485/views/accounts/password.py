"""Change password page for logged in users."""
import flask
from flask import request
import insta485
from insta485.views.accounts.check_password import check_password, hash_password



@insta485.app.route('/accounts/password/', methods=['GET', 'POST'])
def show_password():
    """Display /accounts/password."""
    if request.method == 'POST':
        return do_the_password()
    else:
        return show_the_password_form()


def do_the_password():
    """Display login."""
    return "You are logged in!"


def show_the_password_form():
    """Display /accounts/password form."""
    return flask.render_template("password.html")


@insta485.app.route('/accounts/auth/', methods=['GET', 'POST'])
def edit_password():
    """Edit password."""
    if 'username' not in flask.session:
        return flask.redirect(flask.url_for('show_login'))
    
    if request.method == 'POST':
        password = request.form.get('password')
        password = hash_password(password)

        new_password1 = request.form.get('new_password1')
        new_password2 = request.form.get('new_password2')
        if new_password1 != new_password2:
            return flask.render_template("edit_password.html", error="New passwords do not match.")
        connection = insta485.model.get_db()
        cur = connection.execute(
            "SELECT * FROM users WHERE username = ?",
            (flask.session['username'],)
        )
        user = cur.fetchone()
        if not check_password(user['password'], password):
            return flask.render_template("password.html", error="Incorrect password.")
        new_password = hash_password(new_password1)
        cur = connection.execute(
            "UPDATE users SET password = ? WHERE username = ?",
            (new_password, flask.session['username'])
        )

        return flask.redirect(flask.url_for('show_index'))
    else:
        print("GET " + flask.session['username'])
        return flask.render_template("edit_password.html")
