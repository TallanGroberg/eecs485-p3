import React from "react";
import { useState, useEffect } from "react";
import PropTypes from "prop-types";
import Comment from "./Comment";

const Comments = ({ comments }) => {
  return (
    <>
      {comments.map((comment) => (
        <>
          <Comment key={comment.commentid} comment={comment} />
        </>
      ))}
    </>
  );
};

Comments.propTypes = {
  comments: PropTypes.array.isRequired,
};

export default Comments;
