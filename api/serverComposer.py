from flask import Flask
from flask_cors import CORS

class server:    
    def getServer():
        app = Flask(__name__)
        CORS(app)
        return app


