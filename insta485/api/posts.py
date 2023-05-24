# """REST API for posts."""
# import flask
# import insta485

# @insta485.app.route('/api/v1/')
# def get_resources():
#     """Return API resource URLs."""
#     resources = {
#         "posts": "/api/v1/posts/",
#         "comments": "/api/v1/comments/",
#         "likes": "/api/v1/likes/",
#         "url": "/api/v1/"
#     }
#     print(flask.jsonify(resources), "XXXXXXX")
#     return flask.jsonify(resources)

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

# # # fix user authentication 
# # @insta485.app.route('/api/v1/posts/<int:postid_url_slug>/')
# # def get_posts(postid_url_slug):
# #     """Return 10 newest post urls and ids"""

# #     # Retrieve the 10 newest posts that meet the criteria
# #     posts = query_newest_posts(logged_in_user)

# #     results = [
# #         {"postid": post.postid, "url": f"/api/v1/posts/{post.postid}/"}
# #      ]
# #     return flask.jsonify(result)



