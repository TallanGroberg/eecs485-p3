"""Delete account page."""
import flask
from flask import request
import insta485


@insta485.app.route('/accounts/delete/', methods=['GET', 'POST'])
def show_delete():
    """Display /accounts/delete."""
    if request.method == 'POST':
        return do_the_delete()
    else:
        return show_the_delete_form()


def do_the_delete():
    """Account properly deleted."""
    return "You deleted!"


def show_the_delete_form():
    """Display /accounts/delete form."""
    return flask.render_template("delete.html")
