

function fetch_post(url, setPost, setLikes,setComments) {

    let ignoreStaleRequest = false;

    fetch(url, { credentials: 'same-origin' } )
      .then((response) => {
        if (!response.ok) throw Error(response.statusText);
        return response.json();
      })
      .then((data) => {
        if (!ignoreStaleRequest) {
            setPost(data);
            setLikes(data.likes);
            setComments(data.comments);
          }
        })
        .catch((error) => console.error(error));
    
}

function likePost(postid, setPost, setLikes, setComments) {
  fetch(`/api/v1/likes/?postid=/${postid}/`, {
    method: 'POST',
    credentials: 'same-origin',
  })
  .then((response) => {
    if (!response.ok) throw Error(response.statusText);
    return response.json();
  }
  )
  .then((data) => {
    console.log(data)
    // fetch_post(url, setPost, setLikes, setComments);
  })
  .catch((error) => console.error(error));

}

module.exports = { 
    fetch_post,
    likePost
} ;