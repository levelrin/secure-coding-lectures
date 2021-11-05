# SQL Injection

We are going to demonstrate how SQL injection works.

### Prerequisite

To follow this document, we need to install the following:
1. [Docker](https://docs.docker.com/get-docker/)
2. [Docker Compose](https://docs.docker.com/compose/install/)

### Setup

First, let's set up the environment.
We will use Postgres for the database and Python Flask for the webserver.
Please go to the `sql-injection` directory where this document file exists and execute the following command to build the image for the webserver:
```
docker-compose build
```
We should see the `sql-injection-web:1` image as a result:
```
$ docker images
REPOSITORY          TAG                   IMAGE ID       CREATED              SIZE
sql-injection-web   1                     9bb08fd6084a   About a minute ago   324MB
```

Second, let's run the database and the container for running the web application using the following command:
```
docker-compose up -d
```
We should see our containers running:
```
$ docker ps -a
CONTAINER ID   IMAGE                 COMMAND                  CREATED         STATUS         PORTS                    NAMES
d36f0eb45890   sql-injection-web:1   "tail -f /dev/null"      4 seconds ago   Up 2 seconds   0.0.0.0:5000->5000/tcp   sql-injection-sql-injection-web-1
c2e6f220037c   postgres:13.2         "docker-entrypoint.s…"   4 seconds ago   Up 3 seconds   0.0.0.0:5432->5432/tcp   sql-injection-sql-injection-db-1
```

Third, let's get into the `sql-injection-sql-injection-web-1` container using the following command:
```
docker container exec -it sql-injection-sql-injection-web-1 /bin/bash
```

Now, we are in the web container's shell :)
```
$ docker container exec -it sql-injection-sql-injection-web-1 /bin/bash
root@d36f0eb45890:/usr/share/sql-injection-web# pwd
/usr/share/sql-injection-web
```

In the web container's shell, let's create the `users` table with the `setup.py` script like this:
```
python setup.py
```

Let's check if the database is updated correctly.
Please open a new terminal and execute the following command:
```
docker container exec -it sql-injection-sql-injection-db-1 psql -U postgres -d sql-injection
```
Now, we are in the db container's psql terminal :)
```
$ docker container exec -it sql-injection-sql-injection-db-1 psql -U postgres -d sql-injection
psql (13.2 (Debian 13.2-1.pgdg100+1))
Type "help" for help.

sql-injection=#
```

In the psql terminal, we can confirm that the `users` table exists:
```
sql-injection=# \dt
 public | users | table | postgres
```

cool, we are ready to mess around with the system :P

### Attack

Let's run the vulnerable server.
In the web container's shell, we can run the server using the following commands:
```
export FLASK_APP=bad
flask run --host 0.0.0.0
```

We can see the webpage from the host machine at `http://localhost:5000/`.

From that webpage, we can register a new user. Let's say we put "test01" for the id and "One" for the name.
Once we click the Register button, it should add the user information to the database.
Let's go back to the db container's psql terminal and confirm like this:
```
sql-injection=# table users;
   id   | name
--------+------
 test01 | One
(1 row)

```

Please add more users before hacking the site xD

...played enough? Let's perform the SQL injection :)

Let's put the following information on the website:
```
id:
whatever id

name:
whatever name'); TRUNCATE users; INSERT INTO users (id, name) VALUES ('BOOM!', 'You have got trolled :P
```

After clicking the register button, let's check the database again like this:
```
sql-injection=# table users;
  id   |          name
-------+-------------------------
 BOOM! | You have got trolled :P
(1 row)

```

We've hacked the site successfully xD

Please see the comments written in the `bad.py` if you want to know how it works.

### Secure Coding

There is another web application file called `good.py`.
It's exactly the same as the `bad.py` except the code is written in a secure way.
Please check the comments written in the `good.py` to see the solution.

Let's confirm if the website is no longer vulnerable to SQL injection attacks.
Please go to the web container's shell and press `Ctrl + C` on your keyboard to stop the vulnerable website.
Next, let's run the secure website by executing the following commands:
```
export FLASK_APP=good
flask run --host 0.0.0.0
```

Once again, we can access the website from the host machine at `http://localhost:5000/`.

Please register users and perform the SQL injection attack.
After the attack, we can confirm that the database is secured:
```
sql-injection=# table users;
     id      |                                                  name
-------------+---------------------------------------------------------------------------------------------------------
 test01      | One
 whatever id | whatever name'); TRUNCATE users; INSERT INTO users (id, name) VALUES ('BOOM!', 'You have got trolled :P
(2 rows)

```

### Close

We are done with studying SQL injection :)

We can use' exit' commend to close the web container's shell and db container's psql terminal.
After that, we should execute the following command to stop the containers:
```
docker-compose down
```
Furthermore, we no longer need the `sql-injection-web:1` image. Let's delete it by the following command:
```
docker rmi sql-injection-web:1
```

That's it. Thank you for reading this document :)
