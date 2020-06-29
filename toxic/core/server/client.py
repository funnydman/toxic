import socket


class Client:
    HOST = ''
    PORT = 9000

    def __init__(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((self.HOST, self.PORT))
            # data = b"GET / HTTP/1.1\r\n" + b"Content-Type:  application/json\r\n" + b"\r\n" + b"my data"
            data = b'GET / HTTP/1.1\r\n\r\n'
            s.sendall(data)


Client()
