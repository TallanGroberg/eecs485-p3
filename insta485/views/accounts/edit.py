"""Edit account page for logged in user."""
import flask
from flask import request
import insta485


@insta485.app.route('/accounts/edit/', methods=['GET', 'POST'])
def show_edit():
    """Display /accounts/edit."""
    if request.method == 'POST':
        return do_the_edit()
    else:
        return show_the_edit_form()


def do_the_edit():
    """Edit account."""
    return "You did the edit in!"


def show_the_edit_form():
    """Display /accounts/edit form."""
    return flask.render_template("edit.html")
