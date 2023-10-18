from flask import Flask
from flask_cors import CORS

class Server:    
    def getServer():
        app = Flask(__name__)
        CORS(app)
        return app


