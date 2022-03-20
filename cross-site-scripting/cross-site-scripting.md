# Cross-Site Scripting

We are going to study how cross-site scripting (XSS) attacks work.

### Prerequisite

To follow this document, we need to install the following:
1. [Docker](https://docs.docker.com/get-docker/)

### Setup

Let's build a Docker image that contains the necessary environment.
Please open the terminal and go to the directory where this file exists.
And we can build the image like this:
```
docker build -t cross-site-scripting:1 .
```

After building the image, let's run the container like this:
```
docker run --rm --name cross-site-scripting -v ${PWD}:/usr/share/cross-site-scripting -p 5000:5000 -it cross-site-scripting:1 /bin/bash
```
We should be in the container's shell.

Let's go to the directory where the source code for the web application exists:
```
cd /usr/share/cross-site-scripting
```

We are ready to discuss the cross-site scripting.

### Attack

We can run the web application like this:
```
export FLASK_APP=bad
flask run --host 0.0.0.0
```

We can access the web application via `http://localhost:5000`.

This website displays what you type in the input box.
For example, you can put "Yoi Yoi" in the input box and click the `post` button.
You will be navigated into the page where you can see the text "Yoi Yoi".

The issue is that the website displays the user input without any sanitization.
For example, please try the following input:
```
<script>alert("Yoi Yoi");</script>
```
You will see the alert message because your input is wrapped in a `<script>` tag.
That means the hacker can execute the arbitrary JavaScript code.

### Secure Coding

There is another web application file called `good.py`.
It's the same as the `bad.py` except the code is written securely.
Please check the code written in the `good.py` to see the solution.

Let's confirm if the website is no longer vulnerable.
Please go to the container's shell and press `Ctrl + C` on your keyboard to stop the vulnerable website.
Next, let's run the secure website by executing the following commands:
```
export FLASK_APP=good
flask run --host 0.0.0.0
```

Once again, we can access the website from the host machine at `http://localhost:5000/`.

You will no longer be able to inject javascript code into the website.

### Close

We are done with studying the cross-site scripting.

We can use 'exit' commend to close the container's shell.
Furthermore, we no longer need the `cross-site-scripting:1` image. Let's delete it by the following command:
```
docker rmi cross-site-scripting:1
```

That's it. Thank you for reading this document :)
