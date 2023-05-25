"""REST API for posts."""
import flask
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

# still need user authentication 
# def query_database_post(user_log):
#     "Query database for postid/url"
#     connection = insta485.model.get_db()
    
#     #spec: "each post is made by a user which the logged in user follows or the post is made by the logged in user. ""
#     cur = connection.execute(
#         "SELECT postid"
#         "FROM posts"
#         "ORDER BY posts.created DESC "
#         "WHERE owner = ?",
#         (user_log,)
#       )
#     posts_id = cur.fetchall()
      
#     cur2 = connection.execute(
#         "SELECT postid"
#         "FROM posts"
#         "ORDER BY posts.created DESC "
#         "WHERE owner IN (SELECT username FROM following WHERE follower = ?)",
#         (user_log,)
#       )
#     postsid_following = cur2.fetchall()
#     postsid = posts_id + postsid_following
#     return postsid

def query_database_post(user_log, postid_lte=None, size=10, page=1):
    """Query database for postid/url."""
    connection = insta485.model.get_db()

    # Retrieve posts made by the logged in user or users they follow in one query
    query = (
        "SELECT postid "
        "FROM posts "
        "WHERE owner = ? "
        "OR owner IN (SELECT username FROM following WHERE follower = ?) "
        "ORDER BY created DESC"
    )
    params = (user_log, user_log)
    cur = connection.execute(query, params)
    posts_id = cur.fetchall()

    # Apply postid_lte 
    if postid_lte is not None:
        posts_id = [post for post in posts_id if post[0] <= postid_lte]

    # Apply pagination
    offset = (page - 1) * size
    limited_posts_id = posts_id[offset:offset + size]

    return [post[0] for post in limited_posts_id]


@insta485.app.route('/api/v1/posts/')
def get_post():
    """Return 10 newest post urls/ids"""
    if "username" not in flask.session:
      flask.abort(403)

    #Pagination parameters
    postid_lte = request.args.get('postid_lte', default=None, type=int)
    size = request.args.get('size', default=10, type=int)
    page = request.args.get('page', default=1, type=int)

    # error check size and page parameters
    if size < 0 or page < 0:
        response = {
            "message": "Bad Request",
            "status_code": 400
        }
        return flask.jsonify(response), 400
    
    user_log = flask.session['username']

    # Retrieve the 10 posts from func 
    posts = query_database_post(user_log, postid_lte, size, page)
    
    offset = (page - 1) * size
    limited_posts = posts[offset:offset + size]

    results = [
        {"postid": post[0], 
         "url": f"/api/v1/posts/{post[0]}/"}
       for post in limited_posts
     ]
    
    next_page = ""
    if len(posts) > size * page:
        next_page = f"/api/v1/posts/?postid_lte={postid_lte}&size={size}&page={page + 1}"

    response = {
        "next": next_page,
        "results": results,
        "url": flask.request.path + f"?postid_lte={postid_lte}&size={size}&page={page}",
    }
    return flask.jsonify(response), 200





# NOT DONE: COMBINING BOTH POST.PY

"""REST API for posts."""
import flask
from flask import request, redirect, session, jsonify, make_response
import insta485


@insta485.app.route('/api/v1/')
def get_resources():
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
    post = get_1_post(postid)
    return flask.render_template("post.html", **post)

# /api/v1/posts/ - PAGINATION
def query_database_post(user_log, postid_lte=None, size=10, page=1):
    """Query database for postid/url."""
    connection = insta485.model.get_db()
    # Retrieve posts made by the logged in user or users they follow in one query
    cur = connection.execute(
        "SELECT p.postid "
        "FROM posts p "
        "LEFT JOIN following f ON p.owner = f.username2 AND f.username1 = ? "
        "WHERE p.owner = ? OR f.username1 IS NOT NULL "
        "ORDER BY p.postid DESC "
        "LIMIT 10",
        (user_log, user_log)
    )
    posts_id = cur.fetchall()
    print(posts_id)

    # Apply postid_lte 
    if postid_lte is not None:
        posts_id = [post for post in posts_id if post[0] <= postid_lte]

    # Apply pagination
    offset = (page - 1) * size
    limited_posts_id = posts_id[offset:offset + size]
    return [post['postid'] for post in limited_posts_id]

@insta485.app.route('/api/v1/posts/')
def get_posts():
    """Return 10 newest post urls and ids"""
    postid_lte = request.args.get('postid_lte', default=None, type=int)
    size = request.args.get('size', default=10, type=int)
    page = request.args.get('page', default=1, type=int)

    # test case check for posid_lte 1000 not sure what is the max -> 999 
    if size < 0 or page < 0 or (postid_lte is not None and (postid_lte > 999 or postid_lte < 0)):
        response = {
        "message": "Bad Request",
        "status_code": 400
        }
        return flask.jsonify(response), 400
    
    user_log = flask.request.authorization['username']
    posts = query_database_post(user_log, postid_lte, size, page)
    final = []
    for post in posts:
        final.append({ "postid": post,
                        "url": f"/api/v1/posts/{post}/"
                    })
    
    next_page = ""
    if len(posts) > size * page:
        next_page = f"/api/v1/posts/?postid_lte={postid_lte}&size={size}&page={page + 1}"

    response = {
        "next": next_page,
        "results": final,
        "url": flask.request.path + f"?postid_lte={postid_lte}&size={size}&page={page}",
    }

    print(response)
    response = make_response(jsonify(response))
    response.headers["status_code"] = "200 OK"

    return response

    # return jsonify(posts=posts, url=request.path)


@insta485.app.route('/api/v1/posts/<int:postid>/')
def get_post(postid):
    """Display /post the post route."""
    return jsonify(get_1_post(postid))

def get_1_post(postid):
    """Display /post the post route."""
    # Connect to the database
    connection = insta485.model.get_db()
    if 'username' not in flask.session:
        return flask.redirect(flask.url_for('show_login'))

    cur = connection.execute(
        "SELECT posts.postid, posts.owner, posts.filename "
        "AS imgUrl, posts.created "
        "FROM posts "
        "WHERE posts.postid = ?",
        (postid,)
    )

    post = cur.fetchone()
    if post is None:
        return {}  # a non-existing post

    post['imgUrl'] = "/uploads/" + post['imgUrl']
    post['postShowUrl'] = '/posts/' + str(postid) + '/'
    post['url'] = '/api/v1/posts/' + str(postid) + '/'
    post['comments'] = []

    cur2 = connection.execute(
        "SELECT comments.commentid, comments.owner, comments.text "
        "FROM comments "
        "WHERE comments.postid = ?",
        (postid,)
    )
    comments = cur2.fetchall()

    for comment in comments:
        comment['lognameOwnsThis'] = comment['owner'] == session['username']
        comment['url'] = '/api/v1/comments/' + str(comment['commentid']) + '/'
        comment['ownerShowUrl'] = '/users/' + comment['owner'] + '/'
        comment['url'] = '/api/v1/comments/' + str(comment['commentid']) + '/'
        post['comments'].append(comment)

    cur3 = connection.execute(
        "SELECT username, filename AS ownerImgUrl "
        "FROM users "
        "WHERE users.username = ?",
        (post['owner'],)
    )
    user = cur3.fetchone()
    if user is not None:
        post['ownerImgUrl'] = "/uploads/" + user['ownerImgUrl']
        post['ownerShowUrl'] = "/users/" + user['username'] + "/"

    return post


# @insta485.app.route('/api/v1/likes/?postid=<postid>', methods=["POST"])
#     if like exists  
#         return 200

#     return 201
