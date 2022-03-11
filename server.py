from os import environ
from socket import create_server, timeout
from threading import Lock, Thread
import time
import mongoDB as db
import responseMessages as rm


class TNTServer:

    def __init__(self, host, port):
        self._mainSock = create_server((host, port))
        self._mainSock.settimeout(5)
        self._passwordsLock = Lock()
        self._connections = {}
        self._connectionsLock = Lock()
        self._BUFFER_SIZE = 2048
        self._threads = []

    def connected_users(self):
        with self._connectionsLock:
            return self._connections

    def turnOn(self):
        self._serving = True
        Thread(target=self._accept).start()

    def shutDown(self):
        self._serving = False

    def _accept(self):
        while self._serving:
            try:
                conn, _ = self._mainSock.accept()
            except timeout:
                print("connectedPlayers: " + str([*self._connections]))

            else:
                print("New connection")
                newClient = Thread(target=self._newConnection, args=(conn, ))
                self._threads.append(newClient.start())

    def _newConnection(self, conn):
        for _ in range(3):
            data = conn.recv(self._BUFFER_SIZE)
            print(data.decode())
            if data.decode() != "":
                type, user, password = data.decode().split(";")
                if self._registerOrLogin(conn, type, user, password):
                    print("connection established")
                    with self._connectionsLock:
                        self._connections[user] = conn
                    print("listen has finished.")
                    break
        else:
            print("connection closed")
            conn.close()

    def _registerOrLogin(self, conn, type, username, password):
        user = db.getUser(username)
        with self._passwordsLock:
            if user is None:  # User does not exist
                if type == "login":  # From login()
                    conn.sendall(rm.message(2).encode())
                    return False
                else:  # from register()
                    db.createUser(username, password)
                    conn.sendall(rm.message(4).encode())
                    print(f"{username} is registered.")
                    return False
            else:  # User exists
                if type == "register":  # From register()
                    conn.sendall(rm.message(1).encode())
                else:  # From login()
                    if user["password"] != password:
                        conn.sendall(rm.message(3).encode())
                        return False
                    else:
                        conn.sendall(rm.message(5).encode())

                        return True


if __name__ == "__main__":
    host = environ.get("HOST", "localhost")
    server = TNTServer(host, 5550)
    server.turnOn()
    while True:
        if len(server.connected_users()) == 3:
            print("3 players are active")
        time.sleep(5)
