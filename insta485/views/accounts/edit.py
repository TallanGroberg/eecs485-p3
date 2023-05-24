"""Edit account page for logged in user."""
import flask
from flask import request, redirect, session, make_response
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
    if flask.session['username'] == None:
        return flask.redirect("/accounts/login/")
    
    file = request.form.get('file')
    fullname = request.form.get('fullname')
    email = request.form.get('email')

    connection = insta485.model.get_db()
    cur = connection.execute(
        "UPDATE users "
        "WHERE username = ? ",
        "SET fullname = ?, email = ?, filename = ?, "
        (fullname, email, file, session['username'])
    )
    connection.commit()

    
    return redirect('/')


def show_the_edit_form():
    """Display /accounts/edit form."""
    user = session['username']
    connection = insta485.model.get_db()
    cur = connection.execute(
        "SELECT fullname, email AS email "
        "FROM users "
        "WHERE username = ? ",
        (user, )
    )
    context = cur.fetchall()
    context = context[0]
    print(context)


    return flask.render_template("edit.html", **context)
