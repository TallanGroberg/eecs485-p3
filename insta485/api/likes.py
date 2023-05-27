"""REST API for posts."""
import flask
from flask import request, session, jsonify
import insta485


# like helpers
def like_exists(postid, user_log):
    """Check exist."""
    connection = insta485.model.get_db()
    cur = connection.execute(
        "SELECT postid "
        "FROM likes "
        "WHERE owner = ? AND postid = ?",
        (user_log, postid)
    )
    result = cur.fetchall()
    # if result is not None and len(result) == 1:
    return bool(result)


def get_like_id(postid, owner):
    """Get like."""
    connection = insta485.model.get_db()
    cur = connection.execute(
        "SELECT likeid FROM likes WHERE postid = ? AND owner = ?",
        (postid, owner)
    )
    result = cur.fetchone()
    if result is not None:
        return result['likeid']
    return None


@insta485.app.route('/api/v1/likes/', methods=['POST'])
def create_like():
    """Create a new 'like' for a specific post."""
    postid = request.args.get('postid', type=int)
    if flask.request.authorization:
        user_log = flask.request.authorization['username']
    else:
        user_log = session['username']

    # Check if the 'like' already exists for the postid
    if like_exists(postid, user_log):
        # Return the existing like with a 200 response - already exists
        likeid = get_like_id(postid, user_log)
        likes = {
            "likeid": likeid,
            "url": f"/api/v1/likes/{likeid}/",
        }
        return jsonify(likes), 200
    # else:
    # Create a new like and return with a 201 response
    path = f"/api/v1/likes/{postid}/"
    owner = user_log
    # postid = postid
    connection = insta485.model.get_db()
    # get number of likes on this post
    cur = connection.execute(
        "SELECT COUNT(*) AS count FROM likes WHERE postid = ?",
        (postid,)
    )
    result = cur.fetchone()
    num_likes = result['count']
    # add login user's like to likes table
    connection.execute(
        # fix: add likesid/created?
        "INSERT INTO likes (owner, postid) "
        "VALUES (?, ?)",
        (owner, postid)
    )
    # lognameLikesThis = False - where does this come in?
    likes = {
        "numLikes": num_likes + 1,
        "lognameLikesThis": True,  # Changed from False to True
        "url": path,
    }
    return jsonify(likes), 201


# delete like helpers
def exists(likeid):
    """Check like."""
    connection = insta485.model.get_db()
    cur = connection.execute(
        "SELECT likeid "
        "FROM likes "
        "WHERE likeid = ?",
        (likeid,)
    )
    result = cur.fetchall()
    return bool(result)


def user_owns_like(likeid, user_log):
    """Check who owns like'."""
    connection = insta485.model.get_db()
    cur = connection.execute(
        "SELECT likeid "
        "FROM likes "
        "WHERE likeid = ? AND owner = ?",
        (likeid, user_log)
    )
    result = cur.fetchall()
    # if result is not None and len(result) == 1:
    return bool(result)


def delete_like_action(likeid):
    """Delete a like in table."""
    connection = insta485.model.get_db()
    connection.execute(
        "DELETE FROM likes WHERE likeid = ?",
        (likeid,)
    )
    connection.commit()


@insta485.app.route('/api/v1/likes/<int:likeid>/', methods=['DELETE'])
def delete_like(likeid):
    """Delete a 'like'."""
    if flask.request.authorization:
        user_log = flask.request.authorization['username']
    else:
        user_log = session['username']
    # Check if the like exists
    if exists(likeid):
        # Check if the user owns the like
        if user_owns_like(likeid, user_log):
            # Delete the like and return a 204 response
            delete_like_action(likeid)
            return jsonify({"message": "Forbidden", "status_code": 204}), 204

            # User does not own the like, return a 403 response
        return jsonify({"message": "Forbidden", "status_code": 403}), 403

        # Like does not exist, return a 404 response
    return jsonify({"message": "Not Found", "status_code": 404}), 404
