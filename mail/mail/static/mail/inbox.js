// When the page loads, load its default state
document.addEventListener('DOMContentLoaded', function() {
        // Use buttons to toggle between views
        document.querySelector('#inbox').addEventListener('click', () => load_mailbox('inbox'));
        document.querySelector('#sent').addEventListener('click', () => load_mailbox('sent'));
        document.querySelector('#archived').addEventListener('click', () => load_mailbox('archive'));
        document.querySelector('#compose').addEventListener('click', compose_email);

        // event listener for button submit
        document.querySelector('#compose-form').onsubmit = send;

        // Check to see if all the compose form fields are filled before allowing a message to send.
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

function openEmail(id) {
        // Show single email view and hide other views
        document.querySelector('#emails-view').style.display = 'none';
        document.querySelector('#compose-view').style.display = 'none';
        const emailSingleView = document.querySelector('#email-single-view');
        emailSingleView.style.display = 'block';

        fetch(`/emails/${id}`)
                .then(response => response.json())
                .then(data => {
                        JSON.stringify(data);
                        getSingleEmail(data);
                });
}

function getSingleEmail(data) {
        // reset innerHTML of div so emails don't stack
        document.querySelector('#email-single-view').innerHTML = '';

        // fetch the required email data and create an element for it
        const element = document.createElement('div');
        element.innerHTML = `
                <div class='email-container-singleview'>
                        <div class='email-line'>
                        <strong>${data.timestamp}</strong>
                        </div>
        
                        <div class='email-line'>
                        <strong>Subject:</strong> ${data.subject}
                        </div>
                        
                        <div class='email-line'>
                        <strong>From:</strong> ${data.sender}
                        </div>
        
                        <div class='email-line'>
                        <strong>To:</strong> ${data.recipients}
                        </div>
                        
                        <hr>
                        <div class='email-line'>
                        ${data.body}
                        </div>
                        <hr>
                        
                        <div class='button-row'>
                                <div class='email-button'>
                                        <input class="btn btn-primary" type="submit" value="Reply"> 
                                </div>
                                <div class='email-button-reply'>
                                        <input class="btn btn-primary" type="submit" value="Archive">    
                                </div>         
                        </div>
                </div>
                `;

        document.querySelector('#email-single-view').append(element);
}

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
        document.querySelector('#email-single-view').style.display = 'none';

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
        // add content to email div
        if (mailbox === 'sent') {
                element.innerHTML = `
                <div class='email-heading-container'>
                        <div class='email-line'><strong> ${email.recipients}</strong></div>
                        <div class='email-line'><strong></strong>${email.subject}</div> 
                </div>
                <div class='email-heading-container-date'>      
                        <div class='email-date'><strong></strong>${email.timestamp}</div>
                </div>
          `;
        } else if (mailbox === 'inbox') {
                element.innerHTML = `
                <div class='email-heading-container'>
                        <div class='email-line'><strong>${email.sender}</strong></div>
                        <div class='email-line'><strong></strong>${email.subject}</div> 
                </div>
                <div class='email-heading-container-date'>      
                        <div class='email-date'><strong></strong>${email.timestamp}</div>
                </div>
          `;
        } else if (email.archived === true) {
                element.innerHTML = `
                <div class='email-heading-container'>
                        <div class='email-line'><strong>${email.sender}</strong></div>
                        <div class='email-line'><strong></strong>${email.subject}</div> 
                </div>
                <div class='email-heading-container-date'>      
                        <div class='email-date'><strong></strong>${email.timestamp}</div>
                </div>`;
        }

        element.addEventListener('click', () => {
                openEmail(email.id);
        });

        if (email.read === true) {
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
                });
        load_mailbox('sent');
}
