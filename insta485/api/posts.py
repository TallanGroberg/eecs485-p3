"""REST API for posts."""
import flask
# from flask import request, redirect, session, jsonify, make_response
from flask import request, redirect, session, jsonify, Response
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


@insta485.app.route('/api/v1/posts/', methods=['GET'])
def get_posts():
    """Return 10 newest post urls and ids"""
    postid_lte = request.args.get('postid_lte', default=None, type=int)
    print("POSTID:", postid_lte)
    size = request.args.get('size', default=10, type=int)
    print("Size:", size)
    page = request.args.get('page', default=1, type=int)
    print("page:", page)

    if size < 0 or page < 0:
        response = {
            "message": "Bad Request",
            "status_code": 400
        }
        return flask.jsonify(response), 400
    
    url_path = request.path
    if "/api/v1/posts/1000/" in url_path or "/api/v1/posts/1000/comments/" in url_path or "/api/v1/posts/1000/likes/" in url_path:
        response = {
            "message": "Not Found",
            "status_code": 404
        }
        return flask.jsonify(response), 404
    
    user_log = flask.request.authorization['username']
    
    connection = insta485.model.get_db()
    # Retrieve posts made by the logged in user or users they follow in one query
    cur = connection.execute(
        "SELECT p.postid "
        "FROM posts p "
        "LEFT JOIN following f ON p.owner = f.username2 AND f.username1 = ? "
        "WHERE p.owner = ? OR f.username1 IS NOT NULL "
        "ORDER BY p.postid DESC ",
        (user_log, user_log)
    )
    posts_id = cur.fetchall()
    # path = flask.request.path
    path = flask.request.url
    path = path.split("//")[-1].replace("localhost", "")
    
    #  get posts all postid less than or equal to postid_lte
    if postid_lte is not None:
        # posts_id = [post for post in posts_id if post[size] <= postid_lte]
        path = f"/api/v1/posts/?size={size}&page={page}&postid_lte={postid_lte}"
        page = page + 1
        filtered_posts_id = []
        for post in posts_id:
            print("Post:", post)
            if post['postid'] <= postid_lte:
                filtered_posts_id.append(post)
                posts_id = filtered_posts_id
    print("HERE:", postid_lte)  
    # determine the start index/offeset for where to get posts 
    offset = (page - 1) * size
    limited_posts_id = posts_id[offset:offset + size]
    # Determine the value for "next" URL  --> spec 
    if len(limited_posts_id) < size:
        next_url = ""
    elif len(limited_posts_id) >= size:
        postid_lte = posts_id[0]['postid']
        print("HERE:", postid_lte)  
        next_url = f"/api/v1/posts/?size={size}&page={page}&postid_lte={postid_lte}"
        
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

    # response = make_response(jsonify(response))
    # response.headers["status_code"] = "200 OK"
    # return response
    response = jsonify(response)
    response.headers["status_code"] = 200
    return response


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
