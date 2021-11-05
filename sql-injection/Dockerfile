FROM python:3.9.7-slim-bullseye

# Install Flask
RUN pip install flask

# Install psycopg2
RUN apt update
RUN apt install libpq-dev gcc -y
RUN pip install psycopg2
