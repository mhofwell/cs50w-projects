// global JavaScript variables
let list = [];
let pageList = [];
let currentPage = 1;
const numberPerPage = 10;
let numberOfPages = 1; // calculates the total number of pages

// next paginate user profile.
// get the profile template
// on load search for the title
// if its a username
// get posts from that user
// display

document.addEventListener('DOMContentLoaded', function() {
        document.querySelector('#following').addEventListener('click', () => paginate('following'));

        if (document.querySelector('#first')) {
                document.querySelector('#first').onclick = firstPage;
                document.querySelector('#next').onclick = nextPage;
                document.querySelector('#previous').onclick = previousPage;
                document.querySelector('#last').onclick = lastPage;
        }

        const postButton = document.querySelector('#post-button');
        const postBody = document.querySelector('#post-body');

        if (postButton) {
                postButton.onclick = post;
                postButton.disabled = true;
        }

        document.addEventListener('keyup', () => {
                if (postBody.value.length === 0) {
                        postButton.disabled = true;
                } else {
                        postButton.disabled = false;
                }
        });

        if (document.querySelector('#follow-button')) {
                document.querySelector('#follow-button').addEventListener('click', () => {
                        const username = document.querySelector('#profile-name').textContent;
                        update(username);
                });
        }
        if (document.querySelector('#title')) {
                const title = document.querySelector('#title');
        }

        if (document.querySelector('#profile-name')) {
                const profileName = document.querySelector('#profile-name').innerText;
                console.log(profileName);
                paginate(profileName);
        }

        if (document.querySelector('h3') && document.querySelector('h3').textContent === 'All Posts') {
                const group = 'all';
                paginate(group);
        }
});

async function paginate(group) {
        try {
                await getPosts(group);
                // then calculate the number of pages and store it in numberOfPages
                await getNumberOfPages();
                // then loadList
                loadList();
        } catch (error) {
                console.error(error);
        }
}

async function update(username) {
        const followButton = document.querySelector('#follow-button');
        if (followButton.innerText === 'Follow Me!') {
                await follow(username);
                followButton.innerText = 'Unfollow';
        } else if (followButton.innerText === 'Unfollow') {
                await unfollow(username);
                followButton.innerText = 'Follow Me!';
        }
}

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

async function getPosts(group) {
        // reset the list array
        list = [];
        // Show the group name
        if (group === 'all') {
                document.querySelector('#title').innerHTML = `<h3>${group.charAt(0).toUpperCase() +
                        group.slice(1)} Posts</h3><hr>`;
        } else if (group === 'following') {
                const newsfeed = document.querySelector('#newsfeed');

                if (newsfeed) {
                        newsfeed.innerHTML = '';
                } else {
                        const profileHeader = document.querySelector('#profile-container');
                        const profilePosts = document.querySelector('#userposts');

                        if (profileHeader && profilePosts) {
                                profileHeader.innerHTML = '';
                                profilePosts.innerHTML = '';
                                const body = document.querySelector('body');
                                const element = document.createElement('div');
                                element.id = 'title';
                                element.className = 'title';
                                body.append(element);
                        }
                }

                document.querySelector('#title').innerHTML = `<h3>${group.charAt(0).toUpperCase() +
                        group.slice(1)}</h3><hr>`;
                const postContainer = document.querySelector('#post-container');

                if (postContainer) {
                        document.querySelector('#post-container').innerHTML = '';
                }
        }
        await fetch(`/posts/${group}`)
                .then(response => response.json())
                .then(data =>
                        data.forEach(userpost => {
                                JSON.stringify(userpost);
                                // add post
                                console.log(userpost);
                                addPost(userpost);
                        })
                );
}

function addPost(userpost) {
        // create an element for the post
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
        // push each HTML element into the list array.
        list.push(element);
}

async function getNumberOfPages() {
        numberOfPages = Math.ceil(list.length / numberPerPage);
}

function nextPage() {
        currentPage += 1;
        loadList();
}

function previousPage() {
        currentPage -= 1;
        loadList();
}

// CAREFUL TO WIRE UP VARIABLES IN EACH FUNCTION!!!!
function firstPage() {
        currentPage = 1;
        loadList();
}

function lastPage() {
        currentPage = numberOfPages;
        loadList();
}

function drawList() {
        if (document.querySelector('#newsfeed')) {
                document.querySelector('#newsfeed').innerHTML = '';
        }
        for (let r = 0; r < pageList.length; r++) {
                if (document.querySelector('#newsfeed')) {
                        document.querySelector('#newsfeed').append(pageList[r]);
                } else if (document.querySelector('#title')) {
                        document.querySelector('#title').appendChild(pageList[r]);
                } else {
                        document.querySelector('#userposts').appendChild(pageList[r]);
                }
        }
}

function loadList() {
        const begin = (currentPage - 1) * numberPerPage;
        const end = begin + numberPerPage;

        pageList = list.slice(begin, end);
        drawList(); // draws out our data
        check(); // determines the states of the pagination buttons
}

function check() {
        document.getElementById('next').disabled = currentPage === numberOfPages;
        document.getElementById('previous').disabled = currentPage === 1;
        document.getElementById('first').disabled = currentPage === 1;
        document.getElementById('last').disabled = currentPage === numberOfPages;
}

async function follow(username) {
        await fetch(`/follow/${username}`, {
                method: 'PUT',
                body: JSON.stringify({
                        follow: true,
                }),
        })
                .then(response => response.json())
                .then(result => console.log(result));
        await updateFollowerCount(username);
}

async function unfollow(username) {
        await fetch(`/follow/${username}`, {
                method: 'PUT',
                body: JSON.stringify({
                        follow: false,
                }),
        })
                .then(response => response.json())
                .then(result => console.log(result));
        await updateFollowerCount(username);
}

async function updateFollowerCount(username) {
        await fetch(`/followcount/${username}`)
                .then(response => response.text())
                .then(text => {
                        console.log(text);
                        document.querySelector('#follower-count').innerText = text;
                });
}

// ///////////////////// Pagination

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

// function unfollow() {}
