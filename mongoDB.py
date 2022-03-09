import os
from typing import Dict
from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv()

# Get you password from .env file
password = os.environ.get("mongoDB-password")
username = "admin"
clusterName = "tnt"
database = "tnt"

# Connect to you cluster
cluster = MongoClient("mongodb+srv://" + username + ":" + password + "@" +
                      clusterName + ".4cjap.mongodb.net/" + database +
                      "?retryWrites=true&w=majority")

# Create a new database in your cluster
db = cluster.TNT

# Create a new collection in you database
userCollection = db.user
championCollection = db.champion


# Create a new champion
def createChampion(name: str, tier: str):
    id = len(list(championCollection.find()))
    champion = {"_id": id, "name": name.capitalize(), "tier": tier}
    championCollection.insert_one(champion)


# Return an existing champion
def getChampion(name: str):
    champion = championCollection.find_one({"name": name.capitalize()})
    return champion


# Create a new user. Password is soted in plain text, so not a secure method.
# Return true if successful, fale otherwise.
def createUser(username: str, password: str):
    # Check if user exists
    if userCollection.find_one({"username": username}) is None:
        id = len(list(userCollection.find()))
        user = {
            "_id": id,
            "username": username,
            "password": password,
            "matchHistory": {}
        }
        userCollection.insert_one(user)
        return True
    else:
        return False


def getUser(username: str):
    user = userCollection.find_one({"username": username})
    return user


createUser("Oskar", "passord")