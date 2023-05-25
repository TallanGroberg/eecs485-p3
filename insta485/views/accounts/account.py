"""
Insta485 account view.

URLs include:
/accounts/*
"""
import flask
import insta485


@insta485.app.route('/accounts/', methods=["POST"])
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
