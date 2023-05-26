import React, { useState, useEffect } from "react";
import PropTypes from "prop-types";
import Comments from "./Comments";
import {fetch_post, likePost } from "./fetches"

// The parameter of this function is an object with a string called url inside it.
// url is a prop for the Post component.
export default function Post({ url }) {
  /* Display image and post owner of a single post */
  const [post, setPost] = useState({});
  const [likes, setLikes] = useState({});
  const [comments, setComments] = useState([]);
  console.log(likes)
  
  useEffect(() => {
    fetch_post(url, setPost, setLikes, setComments);
    return () => {
      ignoreStaleRequest = true;
    };
  }, [url]);
  
  
      let { created, imgUrl, owner, ownerImgUrl, ownerShowUrl, postShowUrl, postid } = post;
      console.log(postid)


      function displayLikes() {
        if(likes.numLikes === 1) {
          return <p>1 like</p>
        } else if(likes.numLikes > 1) {
          return <p>{likes.numLikes} Likes</p>
        } else {
          return <p>0 likes</p>
        }
      }

      function toggleLikes() {
        if(likes.lognameLikesThis) {
          return <button type="button" onClick={() => unlikePost(url, setPost, setLikes, setComments)}>Unlike</button>
        } else {
          return <button type="button" onClick={() => likePost(url, setPost, setLikes, setComments)}>Like</button>
        }
      }
        


      function unlikePost(url, setPost, setLikes, setComments) {
        useEffect(() => {
          fetch(`/api/v1/likes/${postid}/`, {
            method: 'DELETE',
            credentials: 'same-origin',
          })
          .then((response) => {
            if (!response.ok) throw Error(response.statusText);
            return response.json();
          }
          )
          .then((data) => {
            setLikes(data);
          })
          .catch((error) => console.error(error));
          
        }, [likes]);
      }
      
  return (
    <div className="post">
      <div className="post-header">
        <a href={ownerShowUrl}>
          <img src={ownerImgUrl} alt="post_owner_image" width="50" height="50" />
        </a>
        <p>{owner}</p>
        <p>{created}</p>
        </div>
        <a href={postShowUrl}>
          <img src={imgUrl} alt="post_image" />
        </a>
        { displayLikes() }
         {toggleLikes()}
      <Comments comments={comments} />   
    </div>
  );
}

Post.propTypes = {
  url: PropTypes.string.isRequired,
};
