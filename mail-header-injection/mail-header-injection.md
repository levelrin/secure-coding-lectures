# Mail Header Injection

We are going to study how mail header injection attacks work.

### Prerequisite

To follow this document, we need to install the following:
1. [Docker](https://docs.docker.com/get-docker/)

### Setup

Let's build a Docker image that contains the necessary environment.
Please open the terminal and go to the directory where this file exists.
And we can build the image like this:
```commandline
docker build -t mail-header-injection:1 .
```

After building the image, let's run the container like this:
```commandline
docker run --rm --name mail-header-injection -v ${PWD}:/usr/share/mail-header-injection -p 5000:5000 -it mail-header-injection:1 /bin/bash
```
We should be in the container's shell.

Since we are going to talk about mail, we want to set up a mail server.

Let's start the IMAP/POP3 server to read mails:
```commandline
service dovecot start
```

After that, we should start the SMTP server to send mails:
```commandline
postfix start
```

The mail server works locally, which means the users in the operating system are used as the mail accounts as well.

Let's create some users like this:
```commandline
adduser test01
```

The above command will create a user named `test01`.
Let's do the same to create a user named `test02`.

We should have two users in the operating system.
The mail address of those users are `test01@localhost` and `test02@localhost`.
Let's send some mails to the users.

Currently, we are logged in as root user.
Let's switch the user to test01:
```commandline
su - test01
```

We are going to use `mutt`, which is a mail client.
Please execute this:
```commandline
mutt
```

The above command will navigate us to the mail client for test01.
Please send a mail to test02 and quit the mutt.
Note, the input for `To:` should be `test02@localhost`.

After sending a mail, we can check if the mail has been delivered successfully.
Please execute the `exit` command to return to the root user.
Let's switch to test02 and launch mutt again. The message from test01 should be in the mailbox.

After the confirmation, let's go back to the root user.

We are ready to discuss the mail header injection.

### Attack

To demonstrate the mail header injection, we will host a web server that sends mails to the users.
Let's open the new terminal and go to the mail server container like this:
```commandline
docker exec -it mail-header-injection /bin/bash
```

We will be in the same container as the mail server.
Let's go to the directory where the source code for the web application exists:
```commandline
cd /usr/share/mail-header-injection
```

After that, we can run the web application like this:
```commandline
export FLASK_APP=bad
flask run --host 0.0.0.0
```

We can access the web application via `http://localhost:5000`.

The website asks users to enter their email address when they submit the survey.
Let's input the normal value such as `test01@localhost` and submit the survey.
As the result page suggests, we should check the mailbox.
Let's go to the previous terminal where we used `mutt` client.
We should be able to see the email from the web application.

After seeing the normal behavior, let's try to inject the mail header.
This time, we can input the mail headers with line breaks like this:
```
test01%40localhost%0ACc%3A%20test02%40localhost
```

The above input is URL encoded, which is the same as the following:
```
test01@localhost
Cc: test02@localhost
```

As a result, the web server will send the email with the injected mail header.

We can confirm by checking the email again after submitting the survey.
The user `test02` will receive the email unintentionally.

### Secure Coding

There is another web application file called `good.py`.
It's the same as the `bad.py` except the code is written securely.
Please check the code written in the `good.py` to see the solution.

Let's confirm if the website is no longer vulnerable.
Please go to the container's shell where we ran the web application and press `Ctrl + C` on your keyboard to stop the vulnerable website.
Next, let's run the secure website by executing the following commands:
```commandline
export FLASK_APP=good
flask run --host 0.0.0.0
```

Once again, we can access the website from the host machine at `http://localhost:5000/`.

The website is no longer vulnerable to the mail header injection because it uses the standard library to send mails.

### Close

We are done with studying the mail header injection.

We can use 'exit' commend to close each container's shell we opened.
Furthermore, we no longer need the `mail-header-injection:1` image. Let's delete it by the following command:
```commandline
docker rmi mail-header-injection:1
```

That's it. Thank you for reading this document :)
