import os
from api.serverComposer import Server
from flask import jsonify, request, send_file
from flask_cors import CORS
from api.controllers.auth import AuthController
from api.controllers.admin import UserMusicController
from api.mgen import *
app = Server.getServer()
AuthController = AuthController()
UserMusicController = UserMusicController()

@app.route("/public/<path:filename>")
def public(filename):
    app.config['STATIC_FOLDERS'] = ['../public']

    # Get the file
    file_path = os.path.join(app.config['STATIC_FOLDERS'][0], filename)

    # Send the file
    return send_file(file_path)



@app.route('/')
def home():
    return jsonify({ 'version': '0.0.1', 'description': 'Servicio python composer music'  })


@app.route('/auth/login', methods=['POST'])
def login():
    data = request.json
    email = data.get('email')
    password = data.get('password')
    if (email and password):
        if AuthController.validareCredentials(email, password) == False:
            return jsonify({ 'message': 'Credenciales no validas', 'error' : True}) , 400


        return jsonify(AuthController.login(email, password)) , 200

    return jsonify({ "message": "Error: Credenciales invalidas"}) , 400


@app.route('/auth/register', methods=['POST'])
def register():
    data = request.json
    username = data.get('name')
    email = data.get('email')
    password = data.get('password')
    if (username and email and password):
        if (AuthController.existUser(email)):
            return jsonify({"message": "El usuario ya se encuentra registrado", 'error': True}), 400
        return jsonify(AuthController.register(username, email, password)) , 200

    return jsonify({ "message": "Error"}) , 400

@app.route('/auth/forget-password', methods=['POST'])
def forget_password():
    data = request.json
    email = data.get('email')
    if (email):
        return jsonify(AuthController.register(email)) , 200

    return jsonify({ "message": "Error"}) , 400

@app.route('/auth/reset-password', methods=['POST'])
def reset_password():
    data = request.json
    token = data.get('token')
    password = data.get('password')
    if (token and password):
        return jsonify(AuthController.register(token, password)) , 200

    return jsonify({ "message": "Error"}) , 400


@app.route('/admin/music/generate/<string:token>')
def generate_music(token):
    main()
    return f"Music generator for: {token}"

@app.route('/admin/music/list/<string:token>')
def list_music(token):
    return jsonify({ 'data' : list(UserMusicController.getListMusicGenerated()) }) , 200


if __name__ == '__main__':
    CORS(app)
    app.run(debug=True)
