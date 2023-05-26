"""
Insta485 account view.

URLs include:
/accounts/*
"""
import flask
import insta485
from insta485.views.accounts.login import require_authentication, do_the_login
from flask import request, redirect, session, make_response, jsonify
import base64
import requests


@insta485.app.route('/accounts/', methods=["POST"])
# @require_authentication    
def show_account():
    """Display /account route."""
    # Connect to database
    target = flask.request.args.get('target')
    print("            hit accounts                   ")
    request.operation = "login"
    if request.method == 'POST' and request.operation == "login":
        print("            hit accounts login                  ")
        return do_the_login(request)


    username = flask.session['username']

    connection = insta485.model.get_db()

    cur = connection.execute(
        "SELECT * "
        "FROM users "
        "WHERE username = ?",
        (username, )
    )
    context = cur.fetchall()



    # Add database info to context
    if target is None:
        return flask.render_template("user.html", **context)
    else:
        return flask.redirect(target)

