"""REST API for posts."""
import flask
from flask import request, session, jsonify
import insta485


@insta485.app.route('/api/v1/')
def get_resources():
    """Return API resource URLs."""
    resources = {
        "posts": "/api/v1/posts/",
        "comments": "/api/v1/comments/",
        "likes": "/api/v1/likes/",
        "url": "/api/v1/"
    }
    print(flask.jsonify(resources), "XXXXXXX")
    return flask.jsonify(resources)


@insta485.app.route('/posts/<int:postid>/', methods=['GET'])
def show_post(postid):
    """Show post."""
    post = get_1_post(postid)
    return flask.render_template("post.html", **post)


@insta485.app.route('/api/v1/posts/', methods=['GET'])
def get_posts():
    """Return 10 newest post urls and ids."""
    postid_lte = request.args.get('postid_lte', default=None, type=int)
    size = request.args.get('size', default=10, type=int)
    page = request.args.get('page', default=1, type=int)

    if size < 0 or page < 0:
        response = {
            "message": "Bad Request",
            "status_code": 400
        }
        return flask.jsonify(response), 400

    # user_log = flask.request.authorization['username']
    if flask.request.authorization:
        user_log = flask.request.authorization['username']
    else:
        user_log = session['username']

    connection = insta485.model.get_db()
    cur = connection.execute(
        "SELECT p.postid "
        "FROM posts p "
        "LEFT JOIN following f ON p.owner = f.username2 AND f.username1 = ? "
        "WHERE p.owner = ? OR f.username1 IS NOT NULL "
        "ORDER BY p.postid DESC ",
        (user_log, user_log)
    )
    posts_id = cur.fetchall()
    path = flask.request.url
    path = path.split("//")[-1].replace("localhost", "")
    #  get posts all postid less than or equal to postid_lte
    if postid_lte is not None:
        path = "/api/v1/posts/?" + \
                f"size={size}&" + \
                f"page={page}&" + \
                f"postid_lte={postid_lte}"
        page = page + 1
        for post in posts_id:
            posts_id = [
                post for post in posts_id if post['postid'] <= postid_lte]
    # determine the start index/offeset for where to get posts
    offset = (page - 1) * size
    limited_posts_id = posts_id[offset:offset + size]
    # Determine the value for "next" URL  --> spec
    if len(limited_posts_id) < size:
        next_url = ""
    elif len(limited_posts_id) >= size:
        postid_lte = posts_id[0]['postid']
        next_url = "/api/v1/posts/?" + \
            f"size={size}&" + \
            f"page={page}&" + \
            f"postid_lte={postid_lte}"
    posts = [post['postid'] for post in limited_posts_id]

    final = []
    for post in posts:
        final.append({
            "postid": post,
            "url": f"/api/v1/posts/{post}/"
        })
    response = {
        "next": next_url,
        "results": final,
        "url": path,
    }
    response = jsonify(response)
    response.headers["status_code"] = 200
    return response


@insta485.app.route('/api/v1/posts/<int:postid>/')
def get_post(postid):
    """Display /post the post route."""
    return get_1_post(postid)


def get_1_post(postid):
    """Display /post the post route."""
    # Connect to the database
    connection = insta485.model.get_db()
    if postid > 999:
        response = {
            "message": "Not Found",
            "status_code": 404
        }
        return flask.jsonify(response), 404

    cur = connection.execute(
        "SELECT posts.postid, posts.owner, posts.filename "
        "AS imgUrl, posts.created "
        "FROM posts "
        "WHERE posts.postid = ?",
        (postid,)
    )

    post = cur.fetchall()
    post[0]['imgUrl'] = "/uploads/" + post[0]['imgUrl']
    post[0]['postShowUrl'] = '/posts/' + str(postid) + '/'
    post[0]['url'] = '/api/v1/posts/' + str(postid) + '/'
    post[0]['comments'] = []
    post[0]['comments_url'] = "/api/v1/comments/?postid=" + str(postid)

    cur2 = connection.execute(
        "SELECT comments.commentid, comments.owner, comments.text "
        "FROM comments "
        "WHERE comments.postid = ?",
        (postid, )
    )
    comments = cur2.fetchall()

    cur4 = connection.execute(
        "SELECT username, filename AS ownerImgUrl "
        "FROM users "
        "WHERE users.username = ?",
        (post[0]['owner'],)
    )
    user = cur4.fetchall()
    post[0]['ownerImgUrl'] = "/uploads/" + user[0]['ownerImgUrl']
    post[0]['ownerShowUrl'] = "/users/" + user[0]['username'] + "/"

    for comment in comments:
        comment['lognameOwnsThis'] = comment['owner'] == user[0]['username']
        comment['url'] = '/api/v1/comments/' + str(comment['commentid']) + '/'
        comment['ownerShowUrl'] = '/users/' + comment['owner'] + '/'
        comment['url'] = '/api/v1/comments/' + str(comment['commentid']) + '/'
        post[0]['comments'].append(comment)

    # get likes
    cur3 = connection.execute(
        "SELECT * "
        "FROM likes "
        "WHERE likes.postid = ?",
        (postid, )
    )
    likes = cur3.fetchall()

    post[0]['likes'] = {}
    post[0]['likes']['numLikes'] = len(likes)
    if likes and user:
        post[0]['likes']['lognameLikesThis'] = (
            likes[0]['owner'] == user[0]['username']
            )
        if likes:
            post[0]['likes']['url'] = (
                '/api/v1/likes/' + str(likes[0]['likeid']) + '/'
            )
        else:
            post[0]['likes']['url'] = None
    else:
        post[0]['likes']['lognameLikesThis'] = False
        post[0]['likes']['url'] = None

    # Add database info to context

    return post[0]
