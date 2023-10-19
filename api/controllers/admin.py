from api.db.connection import Database
client = Database().getConnection()
musicComposerDB = client.musicComposerCollection

filesDb = musicComposerDB.files
class UserMusicController():

    def __init__(self):
        pass
    
    def getListMusicGenerated(self):
        return filesDb.find({}, {'_id': 0})

    def GenerateMusic(self):
        pass

