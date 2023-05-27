"""REST API for comments."""

import flask
from flask import abort, request
from flask.helpers import make_response
import insta485
from insta485.views.accounts.account import check_password


# def authentication_check(username, password, db):
#     """
#     Perform a verification process to determine
#     if the provided username and password are able 
#     to authenticate the user. 
#     In case of a mismatch, terminate the process and return a 403 error.
#     """
#     cursor = db.execute(
#         "SELECT password "  
#         "FROM users "
#         "WHERE username = ?",
#         (username, )
#     )
#     password_hashed = cursor.fetchone()['password']
    
#     if check_password(password_hashed, password) is False:
#         abort(403)

@insta485.app.route('/api/v1/comments/', methods=['POST'])
def posting_comments():
    comment = request.json['text']
    postid = request.args.get('postid')
    
    # Connect to the database
    connection = insta485.model.get_db()
    
    # Access control
    if 'username' in flask.session:
        logname = flask.session['username']
    else:
        abort(403)
    
    # Create the comment for the logged user
    connection.execute(
        "INSERT INTO comments(owner, postid, text) "
        "VALUES (?, ?, ?)",
        (logname, postid, comment)
    )
    cursor = connection.execute(
        "SELECT last_insert_rowid() "
        "FROM comments"
    )
    comment_id = cursor.fetchone()['last_insert_rowid()']
    
    context = {
        "commentid": comment_id,
        "lognameOwnsThis": True,
        "owner": logname,
        "ownerShowUrl" : flask.url_for('user_profile', username=logname, _external=True),
        "text": comment,
        "url" : flask.url_for('get_comment', commentid=comment_id, _external=True)

    }
    return flask.jsonify(**context), 201

@insta485.app.route('/api/v1/comments/<commentid>/', methods=['DELETE'])
def delete_comment(commentid):
    # Connect to the database
    connection = insta485.model.get_db()

    # Access control
    if 'username' in flask.session:
        logname = flask.session['username']
    else:
        abort(403)

    # Check if the commentid exists and if the user owns it
    cursor = connection.execute(
        "SELECT owner "
        "FROM comments "
        "WHERE commentid = ?",
        (commentid,)
    )
    comment = cursor.fetchone()
    if comment['owner'] != logname:
        abort(403)
    elif comment is None:
        abort(404)

    # Delete the comment
    connection.execute(
        "DELETE "
        "FROM comments "
        "WHERE commentid = ?",
        (commentid,)
    )

    return make_response('', 204)






