import socket
import selectors

from phound.logging import logger


class Connection:
    def __init__(self, conn: socket.socket) -> None:
        self.file = conn.makefile('r')
        self._conn = conn

    def close(self) -> None:
        logger.info("Closing connection")
        self.file.close()
        self._conn.close()


class Server:
    def __init__(self) -> None:
        self._sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self._sock.bind(("127.0.0.1", 0))
        self._sock.listen(5)
        self._selector = selectors.DefaultSelector()
        self._selector.register(self._sock, selectors.EVENT_READ)

    def get_new_connection(self) -> Connection:
        # Using selector and infinite loop is required to be able to interrupt listening on windows
        while True:
            events = self._selector.select(timeout=0.5)
            if events:
                conn, _ = self._sock.accept()
                return Connection(conn)

    @property
    def port(self) -> int:
        return self._sock.getsockname()[1]
