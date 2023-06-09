"""
Insta485 account view.

URLs include:
/post/*
"""
import flask
from flask import request, redirect, session
import insta485
import pathlib
import uuid


@insta485.app.route('/api/v1/posts/<int:postid>/')
def show_post(postid):
    """Display /post the post route."""
    # Connect to the database
    connection = insta485.model.get_db()

    cur = connection.execute(
        "SELECT posts.postid, posts.owner, posts.filename, posts.created "
        "FROM posts "
        "WHERE posts.postid = ?",
        (postid,)
    )

    post = cur.fetchall()

    cur2 = connection.execute(
        "SELECT comments.postid, comments.owner, "
        "comments.commentid, comments.text "
        "FROM comments "
        "WHERE comments.postid = ?",
        (postid, )
    )

    cur3 = connection.execute(
        "SELECT filename "
        "FROM users "
        "WHERE users.username = ?",
        (post[0]['owner'],)
    )

    comments = cur2.fetchall()
    post[0]['user_filename'] = cur3.fetchone()['filename']

    cur4 = connection.execute(
        "SELECT filename "
        "FROM users "
        "WHERE users.username = ?",
        (comments[0]['owner'],)
    )
    comments[0]['user_filename'] = cur4.fetchall()
    print(comments[0]['user_filename'])
    # Add database info to context
    context = {"posts": post,
               "comments": comments
               }
    # print(post[0]['user_filename'])


    return flask.render_template("post.html", **context)


@insta485.app.route('/posts/', methods=['POST', 'GET'])
def add_post():
    """Make /post the post route."""
    if 'username' not in flask.session:
        return flask.redirect(flask.url_for('show_login'))
    
    if request.method == 'POST':
        return do_the_post()
    else:
        return show_the_post_form()


def do_the_post():
    # Connect to the database
    target = flask.request.args.get('target')

    connection = insta485.model.get_db()
    filename = handle_file(flask.request.files['file'])

    connection.execute(
        "INSERT INTO posts (owner, filename) "
        "VALUES (?, ?)",
        (flask.session['username'], filename)
    )
    cur = connection.execute(
        "SELECT postid "
        "FROM posts "
        "WHERE posts.owner = ? AND posts.filename = ?",
        (flask.session['username'], filename)
    )

    connection.commit()

    if not target:
        redirect("user/" + flask.session['username'] + "/")
    else:
        return flask.redirect(target[0])

def show_the_post_form():
    """Display /post form."""
    return flask.render_template("create_post.html")


def handle_file(fileobj):
    """Handle file upload."""
    # Unpack flask object
    filename = fileobj.filename

    # Compute base name (filename without directory).  We use a UUID to avoid
    # clashes with existing files, and ensure that the name is compatible with the
    # filesystem. For best practive, we ensure uniform file extensions (e.g.
    # lowercase).
    stem = uuid.uuid4().hex
    suffix = pathlib.Path(filename).suffix.lower()
    uuid_basename = f"{stem}{suffix}"

    # Save to disk
    path = insta485.app.config["UPLOAD_FOLDER"]/uuid_basename
    print(path)
    print(uuid_basename)
    fileobj.save(path)
    return uuid_basename

