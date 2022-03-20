# Directory Traversal Attack

We are going to demonstrate how the directory traversal attack works.

### User Scenario

We will have a website that opens the file on the remote server.
The file path is visible in the URL.

### Prerequisite

To follow this document, we need to install the following:
1. [Docker](https://docs.docker.com/get-docker/)

### Setup

We are going to use Python Flask to create a web application.
Let's open a terminal and go to the directory where this file exists.
The following command can create the necessary environment:
```
docker build -t directory-traversal-attack:1 .
```

We can check if the new image we just built:
```
$ docker images
REPOSITORY                   TAG                   IMAGE ID       CREATED        SIZE
directory-traversal-attack   1                     08660959aa92   6 days ago     133MB
```

We can run the web application using that image like this:
```
docker run --rm --name directory-traversal-attack -v ${PWD}:/usr/share/directory-traversal-attack -p 5000:5000 -it directory-traversal-attack:1 /bin/bash
```

We will end up in the container's terminal:
```
$ docker run --rm --name directory-traversal-attack -v ${PWD}:/usr/share/directory-traversal-attack -p 5000:5000 -it directory-traversal-attack:1 /bin/bash
root@51e6d98ae515:/usr/admin#
```

Currently, we are at the directory where the secret file exists:
```
root@51e6d98ae515:/usr/admin# ls
secret
```

The `secret` file is for the server only, and we must not leak this information to other people such as end-users.

Our web application is supposed to read files at `/usr/local/directory-traversal-attack`:
```
root@51e6d98ae515:/usr/admin# cd /usr/local/directory-traversal-attack/
root@51e6d98ae515:/usr/local/directory-traversal-attack# ls
Hey.txt  Wisdom.txt
```

Lastly, our web application files are located at `/usr/share/directory-traversal-attack`:
```
root@51e6d98ae515:/usr/local/directory-traversal-attack# cd /usr/share/directory-traversal-attack
root@51e6d98ae515:/usr/share/directory-traversal-attack# ls
Dockerfile  bad.py  directory-traversal-attack.md  good.py  templates
```

### Attack

Let's check the behavior of our web application.
We can start the webserver like this:
```
cd /usr/share/directory-traversal-attack
export FLASK_APP=bad
flask run --host 0.0.0.0
```

We can access the web application via `http://localhost:5000`.
We will see the file's content by inputting the file name and clicking the `Open` button.

It's time to hack the server by directory traversal attack and see the server's secret >:)

Let's put `../../admin/secret` and click `Open` button.
Boom! we just got the secret information xD

Please see the content of `bad.py` to see how directory traversal attack was possible.

### Secure Coding

There is another web application file called `good.py`.
It's the same as the `bad.py` except the code is written securely.
Please check the code written in the `good.py` to see the solution.

Let's confirm if the website is no longer vulnerable to directory traversal attacks.
Please go to the container's shell and press `Ctrl + C` on your keyboard to stop the vulnerable website.
Next, let's run the secure website by executing the following commands:
```
export FLASK_APP=good
flask run --host 0.0.0.0
```

Once again, we can access the website from the host machine at `http://localhost:5000/`.
Please perform the same directory traversal attack.
The website is no longer vulnerable to directory traversal attacks.

### Close

We are done with studying the directory traversal attack.

We can use 'exit' commend to close the container's shell.
Furthermore, we no longer need the `directory-traversal-attack:1` image. Let's delete it by the following command:
```
docker rmi directory-traversal-attack:1
```

That's it. Thank you for reading this document :)
