from api.db.connection import Database
client = Database().getConnection()
musicComposerDB = client.musicComposerCollection

class UserMusic():

    def __init__(self):
        pass
    
    def getListMusicGenerated(self):
        pass

    def GenerateMusic(self):
        pass

