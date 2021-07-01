from pymongo import MongoClient
import os
from dotenv import load_dotenv
# connection string to cluster

def connect_to_db():
    # initialize client
    client: MongoClient = MongoClient(os.getenv('MONGODB_URL'))
    # dbs can be accessed through client.{db_name}
    return client

if __name__ == '__main__':
    connect_to_db()
