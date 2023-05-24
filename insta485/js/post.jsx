import React, { useState, useEffect } from "react";
import PropTypes from "prop-types";
import Comments from "./Comments";
// import { set } from "cypress/types/lodash";

// The parameter of this function is an object with a string called url inside it.
// url is a prop for the Post component.
export default function Post({ url }) {
  /* Display image and post owner of a single post */

  const [imgUrl, setImgUrl] = useState("");
  const [ownerImgUrl, setOwnerImgUrl] = useState("");
  const [owner, setOwner] = useState("");
  const [created, setcreated] = useState("");
  const [postid, setPostid] = useState("");
  const [comments, setComments] = useState([]);


  useEffect(() => {
    // Declare a boolean flag that we can use to cancel the API request.
    let ignoreStaleRequest = false;

    // Call REST API to get the post's information
    fetch(url)
      .then((response) => {
        if (!response.ok) throw Error(response.statusText);
        return response.json();
      })
      .then((data) => {
        // If ignoreStaleRequest was set to true, we want to ignore the results of the
        // the request. Otherwise, update the state to trigger a new render.
        if (!ignoreStaleRequest) {
          setImgUrl(data.imgUrl);
          console.log(data);
          setOwner(data.owner);
          setcreated(data.created);
          setOwnerImgUrl(data.ownerImgUrl);
          setPostid(data.postid);
          setComments(data.comments);
          console.log(data);
        }
      })
      .catch((error) => console.error(error));
    return () => {
      // This is a cleanup function that runs whenever the Post component
      // unmounts or re-renders. If a Post is about to unmount or re-render, we
      // should avoid updating state.
      ignoreStaleRequest = true;
    };
  }, [url]);

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
  url: PropTypes.string.isRequired,
};
