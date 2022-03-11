Responses = {
    1: "User already exists.",
    2: "Account does not exsist.",
    3: "Invalid password",
    4: "User is registered.",
    5: "Login successful",
    6: "Start game?",
    7: "Start game with these players: "
}


def message(id: int):
    return Responses[id]
