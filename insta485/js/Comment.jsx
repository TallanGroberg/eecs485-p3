import React from 'react';
import { useState, useEffect } from 'react';
import PropTypes from 'prop-types';

const Comment = ({comment}) => {


    return (
        <div>
            <p>{comment.owner}</p>
            <p>{comment.text}</p>
        </div>
    );
};

Comment.propTypes = {
    comment: PropTypes.object.isRequired,
};

export default Comment;

