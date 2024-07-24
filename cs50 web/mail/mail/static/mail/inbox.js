document.addEventListener('DOMContentLoaded', function() {
  // Use buttons to toggle between views
  document.querySelector('#inbox').addEventListener('click', () => load_mailbox('inbox'));
  document.querySelector('#sent').addEventListener('click', () => load_mailbox('sent'));
  document.querySelector('#archived').addEventListener('click', () => load_mailbox('archive'));
  document.querySelector('#compose').addEventListener('click', compose_email);

  // By default, load the inbox
  load_mailbox('inbox');

  // checking if the user submited the compose email form
  const form = document.querySelector('#compose-form')
  form.addEventListener('submit', function() {

    // prevents the page from refreshing
    event.preventDefault();

    // loading the data
    const recipients = this.querySelector('#compose-recipients').value
    const subject = this.querySelector('#compose-subject').value
    const body = this.querySelector('#compose-body').value.replace(/\n/g, '<br>');

    // sending the data to the api to be preccessed
    fetch('/emails', {
      method: 'POST',
      body: JSON.stringify({
          recipients: recipients,
          subject: subject,
          body: body
      })
    })
      .then(responce => responce.json())
      .then(result => {
        // loading the users sent page
        load_mailbox('sent');
      })

  })
});

function compose_email(sender, recipients, subject, body, timestamp) {

  // importing the current time

  // Show compose view and hide other views
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'block';
  document.querySelector('#email-view').style.display = 'none';

  // checking if this a reply
  if (sender, recipients, subject, body, timestamp){

    // checking for and applying Re:
    let fullSubject
    if (subject.startsWith('Re: ')) {
      fullSubject = subject
    } else {
      fullSubject = 'Re: ' + subject
    }

    // creating the body
    let fullBody

    fetch('/get_user_info')
    .then(response => response.json())
    .then(data => {
      // checking a applying the fullBody
          let currentTime = new Date().toString().split('(')[0];
          let fullBody;
          let moddedbody = body.replace(/<br>/gi, '\n')
          console.log(moddedbody)
          if (body.startsWith(`at`)) {
            fullBody = `at ${moddedbody}\n${data.user_email} replied ${currentTime}:`
          } else {
            fullBody = `at ${timestamp} ${sender} sent:\n${moddedbody}\n${data.user_email} replied at ${currentTime}:`
          }
          document.querySelector('#compose-recipients').value = sender;
          document.querySelector('#compose-subject').value = fullSubject;
          document.querySelector('#compose-body').value = fullBody;
    })




  } else {
    // Clear out composition fields
    document.querySelector('#compose-recipients').value = '';
    document.querySelector('#compose-subject').value = '';
    document.querySelector('#compose-body').value = '';
  }

}

function load_mailbox(mailbox) {

  // Show the mailbox and hide other views
  document.querySelector('#emails-view').style.display = 'block';
  document.querySelector('#compose-view').style.display = 'none';
  document.querySelector('#email-view').style.display = 'none';

  // Show the mailbox name
  document.querySelector('#emails-view').innerHTML = `<h3>${mailbox.charAt(0).toUpperCase() + mailbox.slice(1)}</h3>`;

  // retrieving the mailbox data
  let div = document.querySelector('#emails-view')
  fetch(`/emails/${mailbox}`)
  .then(response => response.json())
  .then(result => {
    console.log(result)

    // itarate over each object
    result.forEach(email => {

      // creating a new div for each email and adding the data
      let element = document.createElement('div');
      element.id = 'mail-div';

      // retriving data about the email
      const sender = email.sender;
      const recipients = email.recipients.join(', ');
      const subject = email.subject;
      const timestamp = email.timestamp;

      element.innerHTML = `<div class="email-content">
                              <hr>
                              <strong>From</strong>: ${sender}<br/>
                              <strong>To</strong>: ${recipients}<br/>
                              <strong>Subject</strong>: ${subject}<br/>
                              <strong>Timestamp</strong>: ${timestamp}
                              <hr>
                          </div>`;

      const insideDiv = element.querySelector('.email-content');

      // checking if the email is read and if ya changing the style
      if (email.read) {
        insideDiv.style.background = '#f1f1f1';
      };

      // creating the clicking on the div functionality
      insideDiv.addEventListener('mouseover', function() {
        insideDiv.style.boxShadow = '0 0 5px rgb(0, 0, 0, 0.3)';
      });

      insideDiv.addEventListener('mouseout', function() {
        insideDiv.style.boxShadow = 'none';
      });

      insideDiv.addEventListener('click', () => displayEmail(email.id, mailbox));

      document.querySelector('#emails-view').append(element);
    })
  });
}

function displayEmail(id, mailbox) {
  // hiding and showing the apropiate views
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'none';
  document.querySelector('#email-view').style.display = 'block';

  // turning the id into a int
  const email_id = parseInt(id);

  // retrieving the data of the email
  fetch(`/emails/${email_id}`)
  .then(responce => responce.json())
  .then(email => {

    // marking as read if the email was not read
    if (email.read !== true) {
      fetch(`/emails/${email_id}`, {
        method: 'PUT',
        body: JSON.stringify({
          read: true
        })
      })
    };

    // retriving data about the email
    const sender = email.sender;
    const recipients = email.recipients.join(', ');
    const subject = email.subject;
    const body = email.body;
    const timestamp = email.timestamp;

    const emailDiv = document.querySelector('#email-view')
    emailDiv.innerHTML = ''

    // updating the html
    const contentToAdd = `<strong>From</strong>: ${sender}<br/>
    <strong>To</strong>: ${recipients}<br/>
    <strong>Subject</strong>: ${subject}<br/>
    <strong>Timestamp</strong>: ${timestamp}
    <hr>
    ${body}
    `

    if (email.archived && mailbox !== 'sent') {
      buttons = '<br><br><button id="archive" class="btn btn-primary" data="false">Unarchive</button><button id="reply" class="btn btn-primary">Reply</button>'
    } else if (mailbox !== 'sent') {
      buttons = '<br><br><button id="archive" class="btn btn-primary" data="true">Archive</button><button id="reply" class="btn btn-primary">Reply</button>'
    } else {
      buttons = '<br><button id="reply" class="btn btn-primary">Reply</button>'
    }

    emailDiv.innerHTML = contentToAdd + buttons

    // adding the archive funcionnality
    const archiveButton = document.querySelector('#archive');
    const replyButton = document.querySelector('#reply');

    if (archiveButton){
      const value = archiveButton.getAttribute('data')
      archiveButton.addEventListener('click', () => archiveFunction(email.id, value));
    }

    replyButton.addEventListener('click', () => compose_email(sender, recipients, subject, body, timestamp));

    console.log(email)
  })
}

// handles archive logic
function archiveFunction(id, action) {
  email_id = parseInt(id)

  // changing the action to a bool
  if (action === "true") {
    boolValue = true;
  } else if (action === "false") {
    boolValue = false;
  }

  // changing the emails archive state
  fetch(`/emails/${email_id}`, {
    method: 'PUT',
    body: JSON.stringify({
      archived: boolValue
    })
  })
    .then(responce =>  {
      console.log('success');
      location.reload();
    })
    .catch(error => {'error', error})
};

