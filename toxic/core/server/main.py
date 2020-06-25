import selectors
from io import BytesIO
from socket import AF_INET, SOCK_STREAM, SOCK_NONBLOCK, socket, SocketIO


class TCPServer:
    address_family = AF_INET
    type = SOCK_STREAM
    option = SOCK_NONBLOCK

    def __init__(self) -> None:
        self.socket = socket(family=self.address_family, type=self.type)

        self.sel = selectors.DefaultSelector()
        self.sel.register(self.socket, selectors.EVENT_READ, self.accept)

    def close(self) -> None:
        self.socket.close()

    def accept(self, sock, mask):
        conn, addr = self.socket.accept()
        self.wfile = conn.makefile('wb', buffering=-1)
        self.rfile = conn.makefile('rb', buffering=-1)
        # there something with read main loop in the SocketIO implementation
        raw = SocketIO(self, 'rb')

        buffer = BytesIO()
        buffer.write(b'some')

        # conn.recv_into(buffer)

        # self.file = conn.makefile('rwb')
        # self.file.write(b'some')
        # self.file.read(1)

        # print(self.rfile.read())

        self.sel.register(conn, selectors.EVENT_READ, self.read)

    def read(self, conn, mask):
        # data = conn.recv(1000)  # read as much as possible
        # self.wfile.write(b'test')
        # data = self.rfile.read(1000)
        data = None
        to_send = b"HTTP/1.1 200 OK\r\nContent-Type: application/json\r\n\r\n{\"name\":\"funnydman\"}\r\n"
        with conn:
            try:
                if data:
                    conn.send(to_send)
            finally:
                self.sel.unregister(conn)
                self.close()

    def write(self):
        pass

    def run(self, host: str, port: int) -> None:
        self.socket.bind((host, port))
        self.socket.listen()

        while True:
            events = self.sel.select()
            for key, mask in events:
                callback = key.data
                callback(key.fileobj, mask)

    def handler(self, conn):
        pass


class HTTPServer(TCPServer):
    pass


if __name__ == '__main__':
    server = HTTPServer()

    server.run(host='', port=5000)
