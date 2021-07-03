"""Echo server module."""

import socket
import sys

from utils import parse_method, parse_status_code, get_status_phrase


def handle_connection(connection: socket.socket, address):
    """Handle connection"""
    data = connection.recv(10000)
    request = data.decode("utf-8")
    headers = request.split("\r\n\r\n")[0].split("\r\n")
    status_line = headers.pop(0)
    method = parse_method(status_line)
    status_code = parse_status_code(status_line)
    status_phrase = get_status_phrase(status_code)

    message = f"HTTP/1.1 {status_code} {status_phrase}\r\n" + \
        "\r\n" + \
        f"Request Method: {method}\r\n" + \
        f"Request Source: ({address[0]}, {address[1]})\r\n" + \
        f"Response Status: {status_code} {status_phrase}\r\n" + \
        "\r\n".join(headers) + \
        "\r\n"

    connection.send(message.encode("utf-8"))


def start_server(host: str, port: int):
    """Start echo server"""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.bind((host, port))
        server_socket.listen()

        while True:
            connection, address = server_socket.accept()
            with connection:
                handle_connection(connection, address)


if len(sys.argv) != 3:
    print("Usage:\n python echo_server.py 127.0.0.1 8989")
    sys.exit(1)

start_server(sys.argv[1], int(sys.argv[2]))
