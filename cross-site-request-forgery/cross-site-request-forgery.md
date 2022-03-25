# Cross-Site Request Forgery

We are going to study how cross-site request forgery (CSRF) attacks work.

### Prerequisite

To follow this document, we need to install the following:
1. [Docker](https://docs.docker.com/get-docker/)

### Setup

Let's build a Docker image that contains the necessary environment.
Please open the terminal and go to the directory where this file exists.
And we can build the image like this:
```
docker build -t csrf:1 .
```

After building the image, let's run the container like this:
```
docker run --rm --name csrf -v ${PWD}:/usr/share/csrf -p 5000:5000 -it csrf:1 /bin/bash
```
We should be in the container's shell.

Let's go to the directory where the source code for the web application exists:
```
cd /usr/share/csrf
```

We are ready to discuss the cross-site request forgery.

### Attack

We can run the web application like this:
```
export FLASK_APP=bad
flask run --host 0.0.0.0
```

We can access the web application via `http://localhost:5000`.

First, let's log in to the web application.
Please use the following credential:
 - username: test01
 - password: 1111

The web application uses a session id to identify the user.
The session id is stored in the cookie, which means the browser will send the session id in the request header automatically for all requests to the domain of this web application.
I highly recommend you to open the DevTools in the browser to see the network traffic in the browser.

After the login, there will be a form to add an item.
Please add the following items (case sensitive):
 - apple
 - banana
 - orange
 
The website should display the list of items you've added.

When you click the `Remove` button, the endpoint `/removeItem` will be called and the server will remove the item from the list.
Of course, the server will check if the request contains the correct session id before doing so.

The hacker can exploit the fact that the browser sends the session id automatically.
For example, let's say the hacker sends an email to you pretending to be the legit website like this:
```
Title: There was an update to your items.

Content:
Hi, test01.
There was an update to your items.
Please check your items via http://localhost:4444.

Thanks,
The legit server
```

The email above is trying to make you click the link.
Note, the fake URL (http://localhost:4444) looks similar to the legit URL (http://localhost:5000).

Once you click the link, the fake website will be opened in your default browser.
You probably used the default browser to access the legit website.
If the fake website access the legit website, your browser will use the session id of the legit website!
You may think that the browser's same origin policy will prevent the fake website from accessing the legit website.
However, the same origin policy behaves like the following:
 - It prevents the *javascript code* from accessing the different domain. That means requests made by HTML `form` are not restricted.
 - It prevents the client from seeing the response. The request itself still goes to the server. That means it's possible to alter the server's state via POST request, for example.

Let's confirm that the hacker can access the legit website via the fake one.
While the legit web application is still running, please open the new terminal and navigate to the directory where this file exists.
After that, run this command:
```
docker run --rm --name attack -v ${PWD}:/usr/share/csrf -p 4444:4444 -it csrf:1 /bin/bash
```
We should be in the container's shell.

Let's go to the directory where the source code for the fake web application exists:
```
cd /usr/share/csrf
```

We can run the fake web application like this:
```
export FLASK_APP=sus
flask run --host 0.0.0.0 --port 4444
```

Next, please open a new tab in your browser and access `http://localhost:4444`.
You will be navigated into the legit website.
Note, the 'apple' has been removed from the list, confirming that you got hacked \(^0^)/

This hacking approach is called `Cross-Site Request Forgery (CSRF)`.

### Secure Coding

There is another web application file called `good.py`.
It's the same as the `bad.py` except the code is written securely.
Please check the code written in the `good.py` to see the solution.

Let's confirm if the website is no longer vulnerable.
Please go to the `bad.py`'s container's shell and press `Ctrl + C` on your keyboard to stop the vulnerable website.
Next, let's run the secure website by executing the following commands:
```
export FLASK_APP=good
flask run --host 0.0.0.0
```

Once again, we can access the website from the host machine at `http://localhost:5000/`.

Note, you will see that every HTML form has an element like this:
```html
<input type="hidden" name="csrf_token" value="IjFlYj...">
```

Now, the server checks two things now:
 - The session ID
 - The CSRF token

Unlike the session ID, the CSRF token is not stored in the cookie.
That's why the fake website no longer able to hack the legit one because it cannot obtain the CSRF token.

### Close

We are done with studying the cross-site request forgery.

We can use 'exit' commend to close the container's shell.
Furthermore, we no longer need the `csrf:1` image. Let's delete it by the following command:
```
docker rmi csrf:1
```

That's it. Thank you for reading this document :)
