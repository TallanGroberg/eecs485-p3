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
