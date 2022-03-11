import threading
import mongoDB as db
import responseMessages as rm


class ClientConnecion(threading.Thread):

    def __init__(self, conn, barrier, connections, connectionsLock,
                 updateDBLock):
        # Call the Thread class's init function
        threading.Thread.__init__(self)
        self.conn = conn
        self.BUFFER_SIZE = 2048
        self.barrier = barrier
        self.connections = connections
        self.connectionsLock = connectionsLock
        self.updateDBLock = updateDBLock

    def run(self):
        for _ in range(3):
            data = self.conn.recv(self.BUFFER_SIZE)
            if data.decode() != "":  # Got some
                type, username, password = data.decode().split(";")
                if type == "register":
                    self.register(username, password)
                elif type == "login":
                    if self.login(username, password):
                        print("connection established")
                        with self.connectionsLock:
                            self.connections[username] = self.conn
                        self.listen()
                        break
                else:
                    print("Login failed")
        else:
            print("connection closed")
            self.conn.close()

    # Try to login player
    def login(self, username, password):
        user = db.getUser(username)
        if user is None:
            self.conn.sendall(rm.message(2).encode())
            return False
        else:
            if user["password"] != password:
                self.conn.sendall(rm.message(3).encode())
                return False
            else:
                self.conn.sendall(rm.message(5).encode())
                return True

    # Register player to database
    def register(self, username, password):
        user = db.getUser(username)
        if user is None:  # No account in database with this username
            with self.updateDBLock:
                db.createUser(username, password)
            self.conn.sendall(rm.message(4).encode())
        else:  # Account already exist.
            self.conn.sendall(rm.message(1).encode())

    def listen(self):
        self.barrier.wait()
        message = "Started game with these players: " + str(
            list(self.connections.keys())) + ". You won!"

        self.conn.sendall(message.encode())


def startGame():
    None