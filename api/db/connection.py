import pymongo

class Database():
    client = pymongo.MongoClient('mongodb+srv://jhon:jhon@cluster0.pimtz.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0')
    def getConnection(self):
        return self.client

