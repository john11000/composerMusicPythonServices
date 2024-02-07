import jwt
import datetime
import uuid
from ..db.connection import Database
#from ..controllers.mgen import MgenController
client = Database().getConnection()
#MgenController = MgenController()
musicComposerDB = client.musicComposerCollection

filesDb = musicComposerDB.files
transcriptDb = musicComposerDB.transcriptFiles
class UserMusicController():

    def __init__(self):
        pass
    
    def changeStateMelody(self, state,  id):
        filesDb.update_one({
                'filename': id,
            }, { "$set": { 'isFavorite': state } })
        return "Melodia añadida a favoritas"
    
    def getListMusicGenerated(self, token):
        payload = jwt.decode(token, 'secret', algorithms=['HS256'])
        email = payload['email']
        return filesDb.find({'email': email}, {'_id': 0})

    def getListMusicGeneratedByUuid(self, file):
            return filesDb.find({
                'uuid': file,
            }, {'_id': 0})

    def GenerateMusic(self, datos, token):
        payload = jwt.decode(token, 'secret', algorithms=["HS256"])
        email = payload['email']
        if datos['pauses'] == 'true':
            datos['pauses'] = True
        else:
            datos['pauses'] = False
        #MgenController.main(email=email, key=datos['key'], num_bars=int(datos['num_bars']), scale= datos['scale'], num_steps=int(datos['num_steps']), num_notes=int(datos['num_notes']), num_mutations=int(datos['nm']), name=datos['name'], root=int(datos['name']), pauses=datos['pauses'], mutation_probability=float(datos['pm']), population_size=int(datos['cm']))
        return "Melodias generadas exitosamente."
    
    def saveTranscript(self, token , text):
        try:
            payload = jwt.decode(token, 'secret', algorithms=["HS256"])
            email = payload['email']
            transcriptDb.insert_one({
            'uuid': str(uuid.uuid4()),
            'email' : email,
            'text': text,
            'createAt': datetime.datetime.now(),
            'updateAt': datetime.datetime.now(),
            })
            return ["Success saved transcript", False]
        except:
           return [ "Error inserting transcript", True]
    def editTranscript(self, file, text):
        try:
            transcriptDb.update_one({
                'uuid': file,
            },{
                '$set': {
                'text': text,
                'updateAt': datetime.datetime.now(),
                }
            })
            return ["Success edited transcript", False]
        except Exception as e:
           print(e)
           return [ "Error edited transcript", True]

    def listTrascript(self, file=0):
        try:
            if (file==0):
                list = transcriptDb.find({}, {'_id': 0})
            else:
                list = transcriptDb.find({'uuid': file}, {'_id': 0})
            return [list, False]
        except Exception as e:
            print(e)
            return [ "Error finding transcript", True]
            


