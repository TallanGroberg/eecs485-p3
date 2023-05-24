"""
Insta485 account view.

URLs include:
/accounts/*
"""
import flask
import insta485
from flask import request


@insta485.app.route('/accounts/', methods=["POST"])
def check_authorization():
    if 'Authorization' not in request.headers:
        return flask.jsonify(message="Unauthorized", status_code=401), 401

    username = flask.request.authorization.get('username')
    password = flask.request.authorization.get('password')

    if not username or not password:
        return flask.jsonify(message="Invalid credentials", status_code=401), 401
    
def show_account():
    """Display /account route."""
    # Connect to database
    target = flask.request.args.get('target')

    if flask.session['username'] == None:
        return flask.redirect("/accounts/login/")

    connection = insta485.model.get_db()
    username = flask.session['username']
    cur = connection.execute(
        "SELECT * "
        "FROM users "
        "WHERE username = ?",
        (username, )
    )
    context = cur.fetchall()

    # Add database info to context
    if target == None:
        return flask.render_template("user.html", **context[0])
    else:
        return flask.redirect(target[0])

