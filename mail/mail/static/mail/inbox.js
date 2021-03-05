// When the page loads, load its default state
document.addEventListener('DOMContentLoaded', function() {
        document.querySelectorAll('.btn-outline-primary').forEach(button => {
                button.onclick = function() {
                        const mailbox = this.id;

                        // Add the current state to the history
                        history.pushState({ mailbox }, '', `/emails/${mailbox}`);
                        if (mailbox !== 'compose') {
                                load_mailbox(mailbox);
                        } else {
                                compose_email();
                        }
                };
        });

        document.querySelector('#compose-form').onsubmit = send;

        // Check to see if all the fields are filled before allowing a message to send.
        document.querySelector('#submit').disabled = true;

        const to = document.querySelector('#compose-recipients');
        const subject = document.querySelector('#compose-subject');
        const body = document.querySelector('#compose-body');

        document.addEventListener('keyup', () => {
                if (to.value.length > 0 && subject.value.length > 0 && body.value.length > 0) {
                        document.querySelector('#submit').disabled = false;
                } else {
                        document.querySelector('#submit').disabled = true;
                }
        });

        // By default, load the inbox
        load_mailbox('inbox');
});

window.onpopstate = function(event) {
        console.log(event.state.mailbox);
        if (event.state.mailbox !== 'compose') {
                load_mailbox(event.state.mailbox);
        } else {
                compose_email();
        }
};

function compose_email() {
        // Show compose view and hide other views
        document.querySelector('#emails-view').style.display = 'none';
        document.querySelector('#compose-view').style.display = 'block';

        // Clear out composition fields
        document.querySelector('#compose-recipients').value = '';
        document.querySelector('#compose-subject').value = '';
        document.querySelector('#compose-body').value = '';
}

function load_mailbox(mailbox) {
        // Show the mailbox and hide other views
        document.querySelector('#emails-view').style.display = 'block';
        document.querySelector('#compose-view').style.display = 'none';

        // Show the mailbox name
        document.querySelector('#emails-view').innerHTML = `<h3>${mailbox.charAt(0).toUpperCase() +
                mailbox.slice(1)}</h3><hr>`;

        fetch(`/emails/${mailbox}`)
                .then(response => response.json())
                .then(data =>
                        data.forEach(email => {
                                JSON.stringify(email);
                                addEmail(email, mailbox);
                        })
                );
}

function addEmail(email, mailbox) {
        // create new email
        const element = document.createElement('div');
        element.className = 'email';
        console.log(email.read);
        // add content to email div
        if (mailbox === 'sent') {
                element.innerHTML = `
          <div class=email-heading-container>
                <div class=email-line><strong> ${email.recipients}</strong></div>
                <div class=email-line><strong></strong>${email.subject}</div> 
          </div>
          <div class=email-heading-container-date>      
                <div class=email-date><strong></strong>${email.timestamp}</div>
          </div>
          `;
        } else if (mailbox === 'inbox') {
                element.innerHTML = `
          <div class=email-heading-container>
                <div class=email-line><strong>${email.sender}</strong></div>
                <div class=email-line><strong></strong>${email.subject}</div> 
          </div>
          <div class=email-heading-container-date>      
                <div class=email-date><strong></strong>${email.timestamp}</div>
          </div>
          `;
        } else if (email.archived === true) {
                element.innerHTML = `
          <div class=email-heading-container>
                <div class=email-line><strong>${email.sender}</strong></div>
                <div class=email-line><strong></strong>${email.subject}</div> 
          </div>
          <div class=email-heading-container-date>      
                <div class=email-date><strong></strong>${email.timestamp}</div>
          </div>`;
        }

        if (email.read === true) {
                console.log(email.read);
                element.classList.add('read');
        }

        document.querySelector('#emails-view').append(element);
}

function send() {
        fetch('/emails', {
                method: 'POST',
                body: JSON.stringify({
                        recipients: document.querySelector('#compose-recipients').value,
                        subject: document.querySelector('#compose-subject').value,
                        body: document.querySelector('#compose-body').value,
                }),
        })
                .then(response => response.json())
                .then(result => {
                        console.log(result);
                        load_mailbox('inbox');
                });
}
