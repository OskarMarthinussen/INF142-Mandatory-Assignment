import pymongo
from pymongo import MongoClient
from dotenv import load_dotenv
load_dotenv()
import os


# Get you password from .env file
password = os.environ.get("password")
username = "oskarmarthinussen"
clusterName = "INF142-Mandatory-Assignment-Cluster"

# Connect to you cluster
client = MongoClient('mongodb+srv://' + username + ':' + password + '@' + clusterName + '.67x6a.mongodb.net/demo-db?retryWrites=true&w=majority')

client = MongoClient('mongodb+srv://oskarmarthinussen:<password>@inf142-mandatory-assign.3ri60.mongodb.net/myFirstDatabase?retryWrites=true&w=majority')



# Create a new database in your cluster
database = client.INF142

# Create a new collection in you database
person = database.person

personDocument = {
  "firstname": "Ola",
  "lastname": "Nordmann",
  "course": "INF142"
}

person.insert_one(personDocument)



