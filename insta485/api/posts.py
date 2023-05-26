"""REST API for posts."""
import flask
from flask import request, redirect, session, jsonify, make_response
import insta485
from insta485.views.accounts.login import require_authentication
import json
from functools import wraps



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


@insta485.app.route('/api/v1/posts/')
@require_authentication
def get_posts():
    """Return 10 newest post urls and ids"""
    print(session)

    connection = insta485.model.get_db()
    cur = connection.execute(
    "SELECT p.postid "
    "FROM posts p "
    "LEFT JOIN following f ON p.owner = f.username2 AND f.username1 = ? "
    "WHERE p.owner = ? OR f.username1 IS NOT NULL "
    "ORDER BY p.postid DESC "
    "LIMIT 10",
    (session['username'],session['username'])
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
    response = jsonify(response)
    

    return response

    # return jsonify(posts=posts, url=request.path)


@insta485.app.route('/api/v1/posts/<int:postid>/')
def get_post(postid):
    """Display /post the post route."""

    return  get_1_post(postid)


def get_1_post(postid):
    """Display /post the post route."""
    # Connect to the database
    connection = insta485.model.get_db()

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
    post[0]['ownerShowUrl'] = "/users/" + user[0]['username'] +  "/"

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

    print("likes:       ",likes)
    post[0]['likes'] = {}
    post[0]['likes']['numLikes'] = len(likes)
    post[0]['likes']['lognameLikesThis'] = likes[0]['owner'] == user[0]['username']
    post[0]['likes']['url'] = '/api/v1/likes/' + str(likes[0]['likeid']) + '/'

    # Add database info to context

    return post[0]


# @insta485.app.route('/api/v1/likes/?postid=<postid>', methods=["POST"])
#     if like exists  
#         return 200

#     return 201



