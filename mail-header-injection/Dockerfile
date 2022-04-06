FROM python:3.9.7-slim-bullseye

# Install Flask
RUN pip install flask

RUN apt update \
    # Install IMAP and POP3 server for reading mails
    && printf '6\n79' | apt install dovecot-imapd dovecot-pop3d -y \
    # Install SMTP server for sending mails
    && printf '5\nlocalhost' | apt install postfix -y \
    # Install mail client
    # mutt needs vim when sending mails
    && apt install -y mutt vim \
    # Clear the apt cache to avoid unintended caching issues in the future
    && rm -rf /var/lib/apt/lists/*
