FROM python:3.9.7-slim-bullseye

# Install Flask
RUN pip install flask

# Create sample text file for the demo
WORKDIR /usr/local/os-command-injection
RUN touch Hey.txt
RUN echo "it's free real estate :)" > Hey.txt
RUN touch Wisdom.txt
RUN echo 'snitches get stitches >:)' > Wisdom.txt

# Create a secret file for the demo
WORKDIR /usr/admin
RUN touch secret
RUN echo 'https://www.youtube.com/watch?v=QtBDL8EiNZo' > secret
