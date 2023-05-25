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


# @insta485.app.route('/api/v1/posts/<int:postid_url_slug>/')
# def get_post(postid_url_slug):
#     """Return post on postid.

#     Example:
#     {
#       "created": "2017-09-28 04:33:28",
#       "imgUrl": "/uploads/122a7d27ca1d7420a1072f695d9290fad4501a41.jpg",
#       "owner": "awdeorio",
#       "ownerImgUrl": "/uploads/e1a7c5c32973862ee15173b0259e3efdb6a391af.jpg",
#       "ownerShowUrl": "/users/awdeorio/",
#       "postShowUrl": "/posts/1/",
#       "url": "/api/v1/posts/1/"
#     }
#     """
#     context = {
#         "created": "2017-09-28 04:33:28",
#         "imgUrl": "/uploads/122a7d27ca1d7420a1072f695d9290fad4501a41.jpg",
#         "owner": "awdeorio",
#         "ownerImgUrl": "/uploads/e1a7c5c32973862ee15173b0259e3efdb6a391af.jpg",
#         "ownerShowUrl": "/users/awdeorio/",
#         "postid": "/posts/{}/".format(postid_url_slug),
#         "url": flask.request.path,
#     }
#     return flask.jsonify(**context)

@insta485.app.route('/posts/<int:postid>/', methods=['GET'])
def show_post(postid):
    post = get_1_post(postid)
    return flask.render_template("post.html", **post)


@insta485.app.route('/api/v1/posts/')

#username = flask.request.authorization['username']
# password = flask.request.authorization['password']
# print (username)
# print (password)
def get_posts():
    """Return 10 newest post urls and ids"""
    # check if user is logged in

    #write a query to get the max postid
    connection = insta485.model.get_db()
    if flask.request.authorization: 
        cur = connection.execute(
            "SELECT p.postid "
            "FROM posts p "
            "LEFT JOIN following f ON p.owner = f.username2 AND f.username1 = ? "
            "WHERE p.owner = ? OR f.username1 IS NOT NULL "
            "ORDER BY p.postid DESC "
            "LIMIT 10",
        (flask.request.authorization['username'],flask.request.authorization['username'])
        )
    else: 
        username = flask.request.form['username']
        password = flask.request.form['password']
        cur = connection.execute(
            "SELECT p.postid "
            "FROM posts p "
            "LEFT JOIN following f ON p.owner = f.username2 AND f.username1 = ? "
            "WHERE p.owner = ? OR f.username1 IS NOT NULL "
            "ORDER BY p.postid DESC "
            "LIMIT 10",
        (flask.request.authorization['username'],flask.request.authorization['username'])
        )

    postids = cur.fetchall()
    print(postids)
    final = []
    for postid in postids:
        # posts.append( get_1_post(postid['postid'] ))
        final.append({ "postid": postid['postid'],
                        "url":'/api/v1/posts/' + str(postid['postid']) + '/'
                    })
    
    response = {
        "next": '',
        "results": final,
        "url": request.path
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


    post = cur.fetchall()
    post[0]['imgUrl'] = "/uploads/" + post[0]['imgUrl'] 
    post[0]['postShowUrl'] = '/posts/' + str(postid) + '/'
    post[0]['url'] = '/api/v1/posts/' + str(postid) + '/'
    post[0]['comments'] = []

    cur2 = connection.execute(
        "SELECT comments.commentid, comments.owner, comments.text "
        "FROM comments "
        "WHERE comments.postid = ?",
        (postid, )
    )
    comments = cur2.fetchall()

    for comment in comments:
        comment['lognameOwnsThis'] = comment['owner'] == session['username']
        comment['url'] = '/api/v1/comments/' + str(comment['commentid']) + '/'
        comment['ownerShowUrl'] = '/users/' + comment['owner'] + '/'
        comment['url'] = '/api/v1/comments/' + str(comment['commentid']) + '/'
        post[0]['comments'].append(comment)

    cur3 = connection.execute(
        "SELECT username, filename AS ownerImgUrl "
        "FROM users "
        "WHERE users.username = ?",
        (post[0]['owner'],)
    )
    user = cur3.fetchall()
    post[0]['ownerImgUrl'] = "/uploads/" + user[0]['ownerImgUrl']
    post[0]['ownerShowUrl'] = "/users/" + user[0]['username'] +  "/"

    # Add database info to context

    print("json ",jsonify(post[0]).data)
    return post[0]


# @insta485.app.route('/api/v1/likes/?postid=<postid>', methods=["POST"])
#     if like exists  
#         return 200

#     return 201




