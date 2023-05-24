"""Delete account page."""
import flask
from flask import request, redirect, session, make_response
import insta485


@insta485.app.route('/accounts/delete/', methods=['GET', 'POST'])
def show_delete():
    """Display /accounts/delete."""

    if flask.session['username'] == None:
        return flask.redirect("/accounts/login/")
    
    if request.method == 'POST':
        return do_the_delete()
    else:
        return show_the_delete_form()


def do_the_delete():
    """Account properly deleted."""
    username = request.form.get('username')
    password = request.form.get('password')
    print(username, password)

    connection = insta485.model.get_db()
    connection.execute(
        "DELETE FROM users WHERE username = ?",
        (session['username'],)
    )
    connection.commit()



    return redirect('/accounts/login/')


def show_the_delete_form():
    """Display /accounts/delete form."""
    return flask.render_template("delete.html")
