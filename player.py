from socket import create_connection
from os import environ
from getpass import getpass
import responseMessages as rm


def connectToServer():
    loginType = input("register[1] or login[2]: ")
    if loginType == "1":
        register()
    elif loginType == "2":
        login(3)
    else:
        print("Bad input, try again")
        connectToServer()


# Quee player up for game
def queueUp():
    print("You are queued up. Waiting for players.")
    sock.sendall("In queue.".encode())
    response = sock.recv(2048).decode()
    print(response)


# Get user input
def getInput():
    username = input("Username: ")
    password = getpass()
    return username + ";" + password


# Register a player in tghe database
def register():
    print("Regisration")
    account = getInput()
    sock.sendall(("register;" + account).encode())
    response = sock.recv(2048).decode()
    if response == rm.message(4):  # If registration is successful
        print("Successful registration")
        login(3)
    else:  # If user already exist
        print(rm.message(1))
        login(3)


# Log player in
def login(attempts: int):
    print("Login")
    account = getInput()
    sock.sendall(("login;" + account).encode())
    response = sock.recv(2048).decode()
    if response == rm.message(2):  # If account does not exist
        print(rm.message(2))
        register()
    elif response == rm.message(3) and attempts > 0:  # Invalid password
        print("Invalid password, try again.")
        login(attempts - 1)
    elif response == rm.message(5):  # Login successful
        print(rm.message(5))
        queueUp()
    else:  # If the user uses too many attempts
        print("Login failed.")


server = environ.get("SERVER", "localhost")
sock = create_connection((server, 5550))
connectToServer()
