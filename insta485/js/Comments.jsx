import React from 'react';
import { useState, useEffect } from 'react';
import PropTypes from 'prop-types';
import Comment from './comment';

const Comments = (url) => {
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
                setComments(data);
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

        comments.map((comment) => (
        <Comment
          key={comment.commentid}
          comment={ [{text: "hello", name: "hello", commentid: 1 } ]  }
          />
          
        ));


    return (<>
        {comments.map((comment) => (
        <Comment
          key={comment.commentid}
          comment={ {text: "hello", name: "hello", commentid: 1 }  }
          />
          
        ))}
    </>
    );
};

Comments.propTypes = {
    url: PropTypes.string.isRequired,
};

export default Comments;