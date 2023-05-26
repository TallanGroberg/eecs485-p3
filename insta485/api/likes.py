"""REST API for posts."""
import flask
from flask import request, session, jsonify
import insta485


def like_exists(postid, user_log):
    connection = insta485.model.get_db()
    cur = connection.execute(
        #fix
        "SELECT EXISTS (SELECT 1 FROM likes WHERE owner = ? AND postid = ?)",
        (user_log, postid)
    )
    result = cur.fetchone()[0]
    return result == 1


@insta485.app.route('/api/v1/likes/?postid=<postid>', methods=["POST"])
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
        path = f"/api/v1/likes/{postid}/"
        likes = {
            "likeid": postid,
            "url": path,
        }
        return jsonify(likes), 200
    else:
        # Create a new like and return with a 201 response
        path = f"/api/v1/likes/{postid}/"
        owner = user_log
        postid = postid
        connection = insta485.model.get_db()
        #get number of likes on this post
        cur = connection.execute(
            "SELECT COUNT(*) FROM likes WHERE postid = ?",
            (postid,)
        )
        result = cur.fetchone()
        num_likes = result[0]
        #add login user's like to like table
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
