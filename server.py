from os import environ
from socket import create_server, timeout
from threading import Lock, Thread, Barrier
from clientConnection import ClientConnecion
import mongoDB as db


class TNTServer:

    def __init__(self, host, port):
        self._mainSock = create_server((host, port))
        self._mainSock.settimeout(3)
        self._connections = {}
        self._connectionsLock = Lock()
        self.updateDBLock = Lock()
        self.barrier = Barrier(4)  # Number of players in a lobby minus server

    # Turn on server
    def turnOn(self):
        self._serving = True
        Thread(target=self._accept).start()

    # Shut down server
    def shutDown(self):
        self._serving = False

    # Accept new connection.
    def _accept(self):
        while self._serving:
            try:
                conn, _ = self._mainSock.accept()
            except timeout:
                print("connectedPlayers: " + str([*self._connections]))

            else:  # Create a new thread for each player trying to connect to the server
                print("New connection")
                ClientConnecion(conn, self.barrier, self._connections,
                                self._connectionsLock,
                                self.updateDBLock).start()


if __name__ == "__main__":
    host = environ.get("HOST", "localhost")
    server = TNTServer(host, 5550)
    server.turnOn()

    while True:
        print("Creating lobby")
        server.barrier.wait()  # wait until lobby is full
        with server._connectionsLock:
            match = {
                "played with: " + str(list(server._connections.keys())): "won"
            }
            for user in server._connections.keys():
                db.updateMatchHistory(user, match)
            server._connections.clear()
        print("Game finished")
        server.barrier.reset()  # Reset lobby
