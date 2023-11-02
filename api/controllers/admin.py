from db.connection import Database
from controllers.mgen import MgenController
client = Database().getConnection()
MgenController = MgenController()
musicComposerDB = client.musicComposerCollection

filesDb = musicComposerDB.files
class UserMusicController():

    def __init__(self):
        pass
    
    def getListMusicGenerated(self):
        return filesDb.find({}, {'_id': 0})

    def GenerateMusic(self, datos):
        MgenController.main(key=datos['key'], num_bars=int(datos['num_bars']))
        return "Melodias generadas exitosamente."

