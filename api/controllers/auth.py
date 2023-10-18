
import hashlib
# Conexion a mongodb
from api.db.connection import Database
client = Database().getConnection()

musicComposerDB = client.musicComposerCollection

usersDb = musicComposerDB.users

class AuthController:

    def login(self, email, password):
        result = self.validareCredentials(email, password)
        if result:
            return {'email': email, 'password': password, 'token': ''}
        return False

    
    def existUser(self, email):
            exist = usersDb.find_one({
                        'email': email,
                    })
            if exist:
                return True
            return False
    
    def validareCredentials(self, email, password):

        user = usersDb.find_one({
                        'email': email
                    })
        
                    # Verificar si se encontró un usuario con las credenciales dadas
        if user :
            print(user)
             # The hash of the encrypted password.
            hashed_password = user['password']

            # Encriptamos la contraseña en texto plano.
            hashed_password_to_verify = hashlib.sha256(password.encode()).hexdigest()

            # Verificamos la contraseña.
            if hashed_password == hashed_password_to_verify:
                return True
            else:
                return False
        else:
            return False
        
       
 
    
    def register(self, username, email, password):

        # Encriptamos la contraseña.
        hashed_password = hashlib.sha256(password.encode()).hexdigest()

        usersDb.insert_one({
            'username': username,
            'email': email,
            'password': hashed_password,
        })
        return {'username': username, 'email': email, 'password': password}
    
    def resetPassword(self, token, password):
        return { 'token': token , 'password': password}
    
    def forgetPassword(self, email):
        return { 'email': email }
    
    
    
    
    