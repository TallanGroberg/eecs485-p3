import React from 'react';
import { useState, useEffect } from 'react';
import PropTypes from 'prop-types';

const Comment = (comment) => {
    const [name, setName] = useState("");
    const [text, setText] = useState("");
    const [commentid, setCommentid] = useState("");

    useEffect(() => {
        setName(comment.name);
        setText(comment.text);
        setCommentid(comment.commentid);

    }, [comment]);

    return (
        <div>
            <p>{name}</p>
            <p>{text}</p>
        </div>
    );
};

// Comment.propTypes = {
//     comment: PropTypes.object.isRequired,
// };

export default Comment;

