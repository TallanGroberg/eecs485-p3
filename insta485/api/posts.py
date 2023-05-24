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


 # "next": "",
  # "results": [
  #   {
  #     "postid": 3,
  #     "url": "/api/v1/posts/3/"
  #   },
  #   {
  #     "postid": 2,
  #     "url": "/api/v1/posts/2/"
  #   },
  #   {
  #     "postid": 1,
  #     "url": "/api/v1/posts/1/"
  #   }
  # ],
  # "url": "/api/v1/posts/"
  
# still need user authentication 
def query_database_post(user_log):
    "Query database for postid/url"
    connection = insta485.model.get_db()
    #spec: "each post is made by a user which the logged in user follows or the post is made by the logged in user. ""
   
    #Fix limit to 10 posts combined? 
    cur = connection.execute(
        "SELECT postid FROM posts WHERE owner = ?",
          (user_log,)
      )
    posts_owner = cur.fetchall()
    
    cur2 = connection.execute(
        "SELECT postid FROM posts WHERE owner IN (SELECT username FROM following WHERE follower = ?)",
        (user_log,)
      )
    posts_following = cur2.fetchall()
    posts = posts_owner + posts_following
    return posts

@insta485.app.route('/api/v1/posts/<int:postid_url_slug>/')
def get_post(postid_url_slug):
    """Return 10 newest post urls/ids"""
    user_log = flask.session['username']
    # Retrieve the 10 posts from func
    posts = query_database_post(user_log)
   
    results = [
        {"postid": posts[0], 
         "url": f"/api/v1/posts/{post[0]}/"}
       for post in posts
     ]
    response = {
        "next": "",
        "results": results,
        "url": flask.request.path,
    }
    return flask.jsonify(response)


