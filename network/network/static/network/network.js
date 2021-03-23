document.addEventListener('DOMContentLoaded', function() {
        document.querySelector('#following').addEventListener('click', () => loadFeed('following'));

        const postForm = document.querySelector('#post-form');
        postForm.disabled = true;
        postForm.onsubmit = post;

        const body = document.querySelector('#post-body');
        const postButton = document.querySelector('#post-button');
        document.addEventListener('keyup', () => {
                if (body.value.length === 0) {
                        postButton.disabled = true;
                } else {
                        postButton.disabled = false;
                }
        });

        loadFeed('all');
});

function follow() {
        const username = document.querySelector('#profile-name').textContent;
        console.log(username);
        // change property of email's read to true
        fetch(`/follow/${username}`, {
                method: 'PUT',
                body: JSON.stringify({
                        follow: true,
                }),
        })
                .then(response => response.json())
                .then(result => {
                        console.log(result);
                });
}

function unfollow() {}

function post() {
        fetch('/post', {
                method: 'POST',
                body: JSON.stringify({
                        body: document.querySelector('#post-body').value,
                }),
        })
                .then(response => response.json())
                .then(result => {
                        console.log(result);
                });
}

function loadFeed(group) {
        // Show the group name
        if (group === 'all') {
                document.querySelector('#title').innerHTML = `<h3>${group.charAt(0).toUpperCase() +
                        group.slice(1)} Posts</h3><hr>`;
        } else if (group === 'following') {
                document.querySelector('#title').innerHTML = `<h3>${group.charAt(0).toUpperCase() +
                        group.slice(1)}</h3><hr>`;
        }
        fetch(`/posts/${group}`)
                .then(response => response.json())
                .then(data =>
                        data.forEach(userpost => {
                                JSON.stringify(userpost);
                                // add post
                                addPost(userpost);
                        })
                );
}

function addPost(userpost) {
        // create an element for the post
        console.log(userpost.id);
        const element = document.createElement('div');
        element.className = 'post';

        // format the element with the appropriate data
        element.innerHTML = `
        <div class="post-wrapper">
                <div class="post-user">
                        <a href="/profile/${userpost.posted_by}">${userpost.posted_by}</a>
                </div>
                <div class="post-body">
                        ${userpost.timestamp}
                </div>
                <div class="post-body">
                        ${userpost.body}
                </div>
                <div class="post-body">
                        ${userpost.likes}
                </div>
                <button type="button" onclick="like()" value="Like" class='btn btn-primary' id="like">Like</button>
        </div>
        `;
        console.log(element);
        // append the element to some parent node on the page.
        document.querySelector('#newsfeed').append(element);
}

// function like() {
//         // create the route to add +1 to the like counter
//         console.log('you liked this post!');
//         return true;
// }

// function updateLikeCounter() {
//         // fetch the new counter number and update the element.
//         console.log('You updated the like counter!');
//         return true;
// }
