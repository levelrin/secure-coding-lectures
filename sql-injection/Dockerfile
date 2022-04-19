FROM python:3.9.7-slim-bullseye

# Install Flask
RUN pip install flask

RUN apt update \
    # Install packages for psycopg2
    && apt install -y libpq-dev gcc \
    # Clear the apt cache to avoid unintended caching issues in the future
    && rm -rf /var/lib/apt/lists/*

# Install psycopg2
RUN pip install psycopg2
