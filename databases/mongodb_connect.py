from pymongo import MongoClient
from pymongo.errors import ConnectionFailure


class MongoDBConnect:
    def __init__(self, mongo_uri, database):
        self.mongo_uri = mongo_uri
        self.database = database
        self.client = None
        self.db = None

    def connect(self):
        try:
            self.client = MongoClient(self.mongo_uri)
            # test connection
            self.client.admin.command('ping')
            self.db = self.client[self.database]
            print(f"----------Connected successfully to MongoDB: {self.database}!---------")
            return self.db
        except ConnectionFailure as e:
            raise Exception(f"---------Fail to connect MongoDB: {e}") from e
    def close(self):
        if self.client:
            self.client.close()
        print("------------------MONGODB Close Connection--------------")
    def __enter__(self):
        self.connect()
        return  self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()