import pymongo
from pymongo import MongoClient
from dotenv import load_dotenv
load_dotenv()
import os


# Get you password from .env file
password = os.environ.get("mongoDB-password")
username = "oskarmarthinussen"
clusterName = "inf142-mandatory-assign"



# Connect to you cluster
client = MongoClient('mongodb+srv://' + username + ':' + password + '@' + clusterName + '.3ri60.mongodb.net/INF142-Mandatory-Assignment?retryWrites=true&w=majority')



# Create a new database in your cluster
database = client.INF142

# Create a new collection in you database
person = database.person

personDocument = {
  "firstname": "Oskar",
  "lastname": "Marthinussen",
  "course": "INF142"
}

person.insert_one(personDocument)



