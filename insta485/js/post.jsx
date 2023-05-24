import React, { useState, useEffect } from "react";
import PropTypes from "prop-types";
import Comments from "./Comments";
// import { set } from "cypress/types/lodash";

// The parameter of this function is an object with a string called url inside it.
// url is a prop for the Post component.
export default function Post({ post }) {
  /* Display image and post owner of a single post */
  const { imgUrl, ownerImgUrl, owner, created,  } = post;
  const [comments, setComments] = useState(post.comments);
  console.log(post.ownerImgUrl);

  console.log(comments);

  // Render post image and post owner
  return (
    <div className="post">
      <div className="post-header">
        <img src={ownerImgUrl} alt="post_owner_image" />
        <p>{owner}</p>
        <p>{created}</p>
        </div>
      <img src={imgUrl} alt="post_image" />
      <Comments comments={comments} />
    </div>
  );
}

Post.propTypes = {
  post: PropTypes.array.isRequired,
};
