import socket
from urllib.parse import unquote

# Create a socket object
s = socket.socket()

# Specify the server address and port.
# The localhost of the Docker container and the localhost of the host machine would be different.
# For that reason, the localhost cannot be used if we are going to run this server inside a Docker container.
# 0.0.0.0 means that the server will listen to all the network interfaces.
# That will allow the host machine to connect to this server via the host machine's localhost.
s.bind(("0.0.0.0", 5000))

# Specify the number of concurrent connections we allow
s.listen(3)

# Keep accepting requests from clients.
while True:
    connection, address = s.accept()
    message = connection.recv(1024).decode()
    request_line = message.splitlines()[0]
    path = request_line.split()[1]
    connection.send(
        bytes(
            """HTTP/1.0 302 FOUND
Content-Type: text/html; charset=utf-8
Content-Length: 7
Location: http://localhost:7777%s
Server: Werkzeug/2.0.2 Python/3.9.7

Yoi Yoi""" % unquote(path),
            "utf-8"
        )
    )
    connection.close()
