
import jwt
import hashlib
import smtplib
from db.connection import Database
from email.message import EmailMessage

# Conexion a mongodb
client = Database().getConnection()
musicComposerDB = client.musicComposerCollection
usersDb = musicComposerDB.users

remitente = "jhon.puentes@qcode.co"
contraseña = "Jhonpololo21."
servidor = "smtp.gmail.com"


class AuthController:

    def login(self, email, password):
        result = self.validareCredentials(email, password)
        if result:
            return {'email': email, 'accessToken':  jwt.encode({'email': email }, "secret", algorithm="HS256")}
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

        return {'username': username, 'email': email, 'accessToken':  jwt.encode({'email': email }, "secret", algorithm="HS256")}
    
    def resetPassword(self, token, password):
        print(token, password)
        payload = jwt.decode(token, "secret", algorithms=["HS256"])
        user = usersDb.find_one({
                                'email': payload['email']
                            })
        if user is not None:
            hashed_password = hashlib.sha256(password.encode()).hexdigest()
            usersDb.update_one({
                'email': payload.email,
            }, { "$set": { 'password': hashed_password } })

        return { 'token': token , 'password': password}
    
    def forgetPassword(self, emailToDeleveri):
        payload = {
            "email": emailToDeleveri,
        }

        user = usersDb.find_one({
                                'email': emailToDeleveri
                            })
        if user is not None:
            token = jwt.encode(payload, "secret", algorithm="HS256")
            email = EmailMessage()
            email["From"] = remitente
            email["To"] = emailToDeleveri
            email["Subject"] = "Recuperar contraseña"
            email.set_content("Para reestablecer la contraseña siga el siguiente link: http://localhost:3002/reset-password?token=" + token) 
            smtp = smtplib.SMTP_SSL(servidor)
            smtp.login(remitente, contraseña)
            smtp.sendmail(remitente, emailToDeleveri, email.as_string())
            smtp.quit()  
        return { 'email': 'correcto' }
    
    
    
    
    