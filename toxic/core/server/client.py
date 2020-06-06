import socket


class Client:
    HOST = ''
    PORT = 8080

    def __init__(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((self.HOST, self.PORT))
            data = b"GET / HTTP/1.1\r\n" + b"Content-Type:  application/json\r\n" + b"\r\n" + b"my data"
            s.sendall(data)


Client()
