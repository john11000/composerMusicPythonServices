import pymongo

class Database():
    client = pymongo.MongoClient('mongodb+srv://jhon:jhon@cluster0.hykao.mongodb.net/?retryWrites=true&w=majority')
    def getConnection(self):
        return self.client

