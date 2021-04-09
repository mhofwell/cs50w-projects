// global JavaScript variables
let list = [];
let pageList = [];
let currentPage = 1;
const numberPerPage = 10;
let numberOfPages = 1; // calculates the total number of pages

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

        if (document.querySelector('#post-form')) {
                document.addEventListener('keyup', () => {
                        if (postBody.value.length === 0) {
                                postButton.disabled = true;
                        } else {
                                postButton.disabled = false;
                        }
                });
        }

        if (document.querySelector('#follow-button')) {
                document.querySelector('#follow-button').addEventListener('click', () => {
                        const username = document.querySelector('#profile-name').textContent;
                        updateFollowButton(username);
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

async function updateFollowButton(username) {
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
                                addPost(userpost);
                        })
                );
}

function addPost(userpost) {
        // create an element for the post
        const element = document.createElement('div');
        const username = document.querySelector('#username').textContent;

        element.className = 'post';
        // format the element with the appropriate data

        if (username !== `${userpost.posted_by}`) {
                element.innerHTML = `
        <div class="post-wrapper">
                <div class="post-user">
                        <a href="/profile/${userpost.posted_by}">${userpost.posted_by}</a>
                </div>
                <div class="post-body">${userpost.timestamp}</div>
                <div class="post-body" id="b${userpost.id}">${userpost.body}</div>
                <div class="post-body" id="c${userpost.id}">${userpost.likes}</div>
                <div class="button-row">
                        <div class="post-button" data-postid="${userpost.id}">
                                <button type="button" data-buttonid="${userpost.id}" value="like" class='btn btn-primary' id="like">Like</button>

                        </div>
                </div> 
        </div>
        `;
        } else {
                element.innerHTML = `
        <div class="post-wrapper">
                <div class="post-user">
                        <a href="/profile/${userpost.posted_by}">${userpost.posted_by}</a>
                </div>
                <div class="post-body">${userpost.timestamp}</div>
                <div class="post-body" id="b${userpost.id}">${userpost.body}</div>
                <div class="post-body" id="c${userpost.id}">${userpost.likes}</div>
                <div class="button-row">
                        <div class="post-button" data-postid="${userpost.id}">
                                <button type="button" data-buttonid="${userpost.id}" value="like" class='btn btn-primary' id="like">Like</button>

                        </div>
                        <div id="e${userpost.id}" class="post-button">
                                <button type="button" data-editid="${userpost.id}" value="edit" class='btn btn-primary' id="edit">Edit</button>

                        </div>
                </div> 
        </div>
        `;
        }

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

async function addLikeListener() {
        document.querySelectorAll('#like').forEach(button => {
                button.addEventListener('click', e => {
                        like(e);
                });
        });
}

function loadList() {
        const begin = (currentPage - 1) * numberPerPage;
        const end = begin + numberPerPage;

        pageList = list.slice(begin, end);
        drawList(); // draws out our data
        addLikeListener(); // adds an event listener for likes.
        addEditListener(); // adds an event listener for editing.
        likeCheck(); // sets the buttons to like or unlike
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

async function like(e) {
        const id = e.target.parentNode.dataset.postid;
        const button = e.target;
        const state = button.innerText;
        let likeBoolean = false;

        if (state === 'Like') {
                button.innerText = 'Unlike';
                likeBoolean = true;
        } else if (state === 'Unlike') {
                button.innerText = 'Like';
                likeBoolean = false;
        }

        await fetch(`/like/${id}`, {
                method: 'PUT',
                body: JSON.stringify({
                        like: `${likeBoolean}`,
                }),
        })
                .then(response => response.json())
                .then(result => {
                        console.log(result);
                });

        await updateLikeCount(id);
}

async function likeCheck() {
        await fetch('/likedposts', {
                method: 'GET',
        })
                .then(response => response.json())
                .then(result =>
                        result.forEach(postId => {
                                if (document.querySelector(`button[data-buttonid="${postId}"]`)) {
                                        document.querySelector(`button[data-buttonid="${postId}"]`).textContent =
                                                'Unlike';
                                }
                        })
                );
}

async function updateLikeCount(id) {
        await fetch(`/likecount/${id}`)
                .then(response => response.text())
                .then(likes => {
                        console.log(likes);
                        document.querySelector(`#c${id}`).innerText = likes;
                });
}

function addEditListener() {
        document.querySelectorAll('#edit').forEach(button => {
                button.addEventListener('click', e => {
                        edit(e);
                });
        });
}

function edit(e) {
        const id = e.target.dataset.editid;
        const body = document.querySelector(`#b${id}`);
        const content = body.textContent;
        const buttonContainer = document.querySelector(`#e${id}`);
        body.innerHTML = `
        <div class="textarea-container">
                <textarea class="body-textarea" style="resize:none" cols="100" rows="5" id="body-textarea">${content}</textarea>
        </div>
        `;

        // replace the save with edit button
        buttonContainer.innerHTML = `<input type="submit" class="btn btn-primary" id="save" value="Save" />`;

        // grab the updated content
        document.querySelector('#save').addEventListener('click', () => {
                const update = document.querySelector('#body-textarea').value;
                console.log(update);
                save(update, id, body);
                buttonContainer.innerHTML = `<button type="button" data-editid="${id}" value="edit" class='btn btn-primary' id="edit">Edit</button>`;
                // re-add the event listener
                document.querySelector(`button[data-editid="${id}"]`).addEventListener('click', n => {
                        edit(n);
                });
        });
}

async function save(update, id, body) {
        console.log(id);
        await fetch(`save/${id}`, {
                method: 'PUT',
                body: JSON.stringify({
                        body: update,
                }),
        })
                .then(response => response.json())
                .then(result => console.log(result));
        await updatePost(update, body);
}

async function updatePost(update, body) {
        body.textContent = update;
}
