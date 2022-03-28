# HTTP Header Injection

We are going to study how HTTP header injection attacks work.

### Prerequisite

To follow this document, we need to install the following:
1. [Docker](https://docs.docker.com/get-docker/)

### Scenario

Let's say we had a website with the domain `http://localhost:5000`.
Now, we moved our website to a new domain `http://localhost:7777`.
Since users may still try to access the old domain, we want to redirect them to the new one.

### Setup

First, we will create a website with the old domain.
Let's build a Docker image that contains the necessary environment.
Please open the terminal and go to the directory where this file exists.
And we can build the image like this:
```
docker build -t http-header-injection:1 .
```

After building the image, let's run the container like this:
```
docker run --rm --name http-header-injection -v ${PWD}:/usr/share/http-header-injection -p 5000:5000 -it http-header-injection:1 /bin/bash
```
We should be in the container's shell.

Let's go to the directory where the source code for the web application exists:
```
cd /usr/share/http-header-injection
```

Note, the name of this container is `http-header-injection`, and it's for running the website with the old domain.

Next, let's prepare the website with the new domain.
Please open the new terminal and go to the directory where this file exists.
Run the second container like this:
```
docker run --rm --name real-site -v ${PWD}:/usr/share/real-site -p 7777:7777 -it http-header-injection:1 /bin/bash
```

We should be in the second container's shell.
Let's go to the directory where the source code for the web application exists:
```
cd /usr/share/real-site
```

Lastly, we can run the website with the new domain like this:
```
export FLASK_APP=real
flask run --host 0.0.0.0 --port 7777
```

We can access the web application via `http://localhost:7777`.

We are ready to discuss the HTTP header injection.

### Attack

Let's run the website with the old domain.
Please go back to the `http-header-injection` container and run the following command:
```
python bad.py
```

We can access the web application via `http://localhost:5000`.
Note, you will be redirected to the new domain `http://localhost:7777`.

Similarly, you will be redirected to `http://localhost:7777/economics` when you access `http://localhost:5000/economics`.

If you examine the source code of `bad.py`, you will realize that the server parses the URL, gets the path, and append that path to the value of `Location` response header.
For example, the path of the `http://localhost:5000/economics` is `/economics`, so the value of `Location` response header would be `http://localhost:7777/economics`.
As a result, the entire response from the server will be:
```
HTTP/1.0 302 FOUND
Content-Type: text/html; charset=utf-8
Content-Length: 7
Location: http://localhost:7777/economics
Server: Werkzeug/2.0.2 Python/3.9.7

Yoi Yoi
```

The browser will redirect you to the new domain `http://localhost:7777/economics`.

The above logic is vulnerable to HTTP header injection.
Consider this URL: `http://localhost:5000/economics%0ALocation%3A%20https%3A%2F%2Fwww.youtube.com%2Fwatch%3Fv%3DxvFZjo5PgG0`

If you use a URL decoder, you will realize that there is a linebreak in the URL.
That URL is equivalent to the following:
```
http://localhost:5000/economics
Location: https://www.youtube.com/watch?v=xvFZjo5PgG0
```

With the above URL, the server will generate the following response:
```
HTTP/1.0 302 FOUND
Content-Type: text/html; charset=utf-8
Content-Length: 7
Location: http://localhost:7777/economics
Location: https://www.youtube.com/watch?v=xvFZjo5PgG0
Server: Werkzeug/2.0.2 Python/3.9.7

Yoi Yoi
```

Note, there are two `Location` response headers, which is still a valid HTTP response.
This is how your browser may lead you to the wrong website instead of the intended destination.

Unfortunately(?), the Chrome browser will protect you from this attack and display the error message `ERR_RESPONSE_HEADERS_MULTIPLE_LOCATION` :(

Still, it's better to make our website secure from the HTTP header injection instead of relying on the browser's protection.

### Secure Coding

There is another web application file called `good.py`.
It's the same as the `bad.py` except the code is written securely.
Please check the code written in the `good.py` to see the solution.
In a nutshell, the `Flask` framework blocks the HTTP header injection out of the box.

Let's confirm if the website is no longer vulnerable.
Please go to the container's shell and press `Ctrl + C` on your keyboard to stop the vulnerable website.
Next, let's run the secure website by executing the following commands:
```
export FLASK_APP=good
flask run --host 0.0.0.0
```

Once again, we can access the website from the host machine at `http://localhost:5000/`.

You can use the above hacky URL again to confirm that the website is no longer vulnerable.

### Close

We are done with studying the HTTP header injection.

We can use 'exit' commend to close the container's shell.
Furthermore, we no longer need the `http-header-injection:1` image. Let's delete it by the following command:
```
docker rmi http-header-injection:1
```

That's it. Thank you for reading this document :)
