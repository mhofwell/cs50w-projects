document.addEventListener('DOMContentLoaded', function() {
        document.querySelector('#following').addEventListener('click', () => loadPosts('following'));

        const postButton = document.querySelector('#post-button');
        postButton.disabled = true;
        postButton.onsubmit = post;
        const body = document.querySelector('#post-body');

        document.addEventListener('keyup', () => {
                if (body.value.length === 0) {
                        postButton.disabled = true;
                } else {
                        postButton.disabled = false;
                }
        });

        loadPosts('all');
});

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
                })
                .then(loadPosts('all'));
}

function loadPosts(group) {
        // Show the group name
        if (group === 'all') {
                document.querySelector('#title').innerHTML = `<h3>${group.charAt(0).toUpperCase() +
                        group.slice(1)} Posts</h3><hr>`;
        } else {
                document.querySelector('#title').innerHTML = `<h3>${group.charAt(0).toUpperCase() +
                        group.slice(1)}</h3><hr>`;
        }

        fetch(`/posts/${group}`)
                .then(response => response.json())
                .then(data =>
                        data.forEach(userpost => {
                                JSON.stringify(userpost);
                                // add post
                                // addEmail(email, mailbox);
                        })
                );
}
