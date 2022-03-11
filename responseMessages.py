# Was too many strings in the files. Made a didctonary to reduce cluttering.
Responses = {
    1: "Account already exists.",
    2: "Account does not exsist.",
    3: "Invalid password",
    4: "User is registered.",
    5: "Login successful",
}


def message(id: int):
    return Responses[id]
