"""Edit account page for logged in user."""
import flask
from flask import request, redirect, session, make_response
import insta485
from insta485.views.post import handle_file
from insta485.views.image import download_file



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


    

    fullname = request.form.get('fullname')
    email = request.form.get('email')
    

    connection = insta485.model.get_db()
    cur = connection.execute(
        "SELECT * "
        "FROM users "
        "WHERE username = ? ",
        (session['username'], )
    )
    user = cur.fetchone()
    
    if flask.request.files['file'] == None or flask.request.files['file'] == "":
        print("CCIONTEKNSDLKFN ",file.content_type)
        print("in if", user['filename'])
        file = download_file(user['filename'])
    else:
        print("CCIONTEKNSDLKFN ",file.content_type)
        print("in else", flask.request.files['file'])
        file = handle_file(flask.request.files['file'])

    if fullname == None or fullname == "":
        fullname = user['fullname']
    if email == None or  email == "":
        email = user['email']


    print(file)
    connection.execute(
        "UPDATE users "
        "SET fullname = ?, email = ?, filename = ? "
        "WHERE username = ? ",
        (fullname, email, file, session['username'])
    )



    connection.execute(
        "UPDATE users "
        "SET fullname = ?, email = ?, filename = ? "
        "WHERE username = ? ",
        (fullname, email, file, session['username'])
    )
    connection.commit()

    cur = connection.execute(
        "SELECT * "
        "FROM users "
        "WHERE username = ? ",
        (session['username'], )
    )
    user = cur.fetchone()



    
    # return redirect("/users/" + session['username'] + "/")
    return flask.redirect("/accounts/edit/")

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


    return flask.render_template("edit.html", **context)
