import React from "react";
import { useState, useEffect } from "react";
import PropTypes from "prop-types";

const Comment = ({ comment }) => {
  console.log(comment.lognameOwnsThis);
  function handleComment() {
    if (comment.lognameOwnsThis) {
      return (
        <button type="button" onClick={() => deleteComment(comment.commentid)}>
          delete Comment
        </button>
      );
    } else {
      return <></>;
    }
  }

  function deleteComment(commentid) {
    fetch(`/api/v1/comments/${commentid}/`, {
      method: "DELETE",
      credentials: "same-origin",
    })
      .then((response) => {
        if (!response.ok) throw Error(response.statusText);
        return response.json();
      })
      .then((data) => {
        console.log(data);
      })
      .catch((error) => console.error(error));
  }

  return (
    <div>
      <p>{comment.owner}</p>
      <p>
        {comment.text} {handleComment()}
      </p>
    </div>
  );
};

Comment.propTypes = {
  comment: PropTypes.object.isRequired,
};

export default Comment;
