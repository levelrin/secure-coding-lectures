# OS Command Injection

We are going to demonstrate how OS command injection works.

### User Scenario

We will have a website that displays the file content on the remote server.
In the backend, the application executes an OS command to read the content of the file.

### Prerequisite

To follow this document, we need to install the following:
1. [Docker](https://docs.docker.com/get-docker/)

### Setup

We are going to use Python Flask to create a web application.
Let's open a terminal and go to the directory where this file exists.
The following command can create the necessary environment:
```
docker build -t os-command-injection:1 .
```

We can check if the new image we just built:
```
$ docker images
REPOSITORY             TAG                   IMAGE ID       CREATED         SIZE
os-command-injection   1                     08660959aa92   8 seconds ago   133MB
```

We can run the web application using that image like this:
```
docker run --rm --name os-command-injection -v ${PWD}:/usr/share/os-command-injection -p 5000:5000 -it os-command-injection:1 /bin/bash
```

We will end up in the container's terminal:
```
$ docker run --rm --name os-command-injection -v ${PWD}:/usr/share/os-command-injection -p 5000:5000 -it os-command-injection:1 /bin/bash
root@65d5d941d5a1:/usr/admin#
```

Currently, we are at the directory where the secret file exists:
```
root@65d5d941d5a1:/usr/admin# ls
secret
```

The `secret` file is for the server only, and we must not leak this information to other people such as end-users.

Our web application is supposed to read files at `/usr/local/os-command-injection`:
```
root@65d5d941d5a1:/usr/admin# cd /usr/local/os-command-injection/
root@65d5d941d5a1:/usr/local/os-command-injection# ls
Hey.txt  Wisdom.txt
```

Lastly, our web application files are located at `/usr/share/os-command-injection`:
```
root@65d5d941d5a1:/usr/local/os-command-injection# cd /usr/share/os-command-injection
root@65d5d941d5a1:/usr/share/os-command-injection# ls
Dockerfile  __pycache__  bad.py  good.py  os-command-injection.md  templates
```

### Attack

Let's check the behavior of our web application.
We can start the webserver like this:
```
cd /usr/share/os-command-injection
export FLASK_APP=bad
flask run --host 0.0.0.0
```

We can access the web application via `http://localhost:5000`.
We will see the file's content by inputting the file name and clicking the `read` button.

It's time to hack the server by OS command injection and see the server's secret >:)

Let's put `Hey.txt && cat /usr/admin/secret` and click `read` button.
Boom! we just got the secret information xD

Please see the content of `bad.py` to see how OS command injection was possible.

### Secure Coding

There is another web application file called `good.py`.
It's the same as the `bad.py` except the code is written securely.
Please check the code written in the `good.py` to see the solution.

Let's confirm if the website is no longer vulnerable to OS command injection attacks.
Please go to the container's shell and press `Ctrl + C` on your keyboard to stop the vulnerable website.
Next, let's run the secure website by executing the following commands:
```
export FLASK_APP=good
flask run --host 0.0.0.0
```

Once again, we can access the website from the host machine at `http://localhost:5000/`.
Please perform the same OS command injection.
The website is no longer vulnerable to OS command injection.

### Close

We are done with studying OS command injection.

We can use' exit' commend to close the container's shell.
Furthermore, we no longer need the `os-command-injection:1` image. Let's delete it by the following command:
```
docker rmi os-command-injection:1
```

That's it. Thank you for reading this document :)
