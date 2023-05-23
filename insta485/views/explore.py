"""
Insta485 account view.

URLs include:
/explore/*
"""
import flask
import insta485


@insta485.app.route('/explore/')
def show_explore():
    """Display /explores route."""
    # Connect to database
    connection = insta485.model.get_db()

    cur = connection.execute(
        "SELECT username, filename "
        "FROM users "
        "WHERE username NOT IN "
        "(SELECT username2 FROM following WHERE username1 = ?) AND username != ? ",
        (flask.session['username'], flask.session['username'])
    )

    users = cur.fetchall()
    print(users)
    # Add database info to context
    context = { "users": users }

    return flask.render_template("explore.html", **context)
