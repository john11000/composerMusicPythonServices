import pymongo

class Database():
    client = pymongo.MongoClient('mongodb+srv://anderson:anderson@cluster0.hykao.mongodb.net/?retryWrites=true&w=majority')
    def getConnection(self):
        return self.client

