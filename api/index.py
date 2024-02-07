import os
from .serverComposer import Server
from flask import jsonify, request, send_file
from flask_cors import CORS
from .controllers.auth import AuthController
from .controllers.admin import UserMusicController as MC

# from api.controllers.mgen import MgenController
app = Server.getServer()
AuthController = AuthController()
UserMusicController = MC()
# MgenControllfrom pydub import AudioSegment

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

@app.route('/auth/forgot-password', methods=['POST'])
def forget_password():
    data = request.json
    email = data.get('email')
    if (email):
        print(email)
        return jsonify(AuthController.forgetPassword(email)) , 200

    return jsonify({ "message": "Error"}) , 400

@app.route('/auth/reset-password', methods=['POST'])
def reset_password():
    data = request.json
    token = data.get('token')
    password = data.get('password')
    if (token and password):
        return jsonify(AuthController.resetPassword(token, password)) , 200

    return jsonify({ "message": "Error"}) , 400


@app.route('/admin/music/generate/<string:token>', methods=["POST"])
def generate_music(token):
    # MgenController.main()
    datos = request.json
    UserMusicController.GenerateMusic(datos=datos, token=token)
    return jsonify({ 'data' : list(UserMusicController.getListMusicGenerated()) }) , 200

@app.route('/admin/music/list/<string:token>')
def list_music(token):
    return jsonify({ 'data' : list(UserMusicController.getListMusicGenerated(token)) }) , 200

@app.route('/admin/music/list/uuid/<string:file>')
def list_music_by_id(file):
    return jsonify({ 'data' : list(UserMusicController.getListMusicGeneratedByUuid(file)) }) , 200

@app.route('/admin/music/favorite', methods=['PUT', 'POST'])
def toggle_favorite():
    datos = request.json
    print(request.headers.get('authorization'))
    if (datos['id']): 
        return jsonify({ 'data' : list(UserMusicController.changeStateMelody(id=datos['id'], state=datos['state'])) }) , 200
    return jsonify({ 'data' : 'Ha ocurrido un error al cambiar los datos', 'isError': True }) , 405


@app.route('/admin/transcript/save', methods=['POST'])
def saveTranscript():
    datos = request.json
    token = datos.get('token')
    text = datos.get('text')
    if (token and text):
        [data, isError] = UserMusicController.saveTranscript(token, text)
        return jsonify({ 'data': data , 'isError': isError}) , 200
    return jsonify({ 'data' : 'Ha ocurrido un error al guardar el texto', 'isError': True }) , 405

@app.route('/admin/transcript/edit', methods=['POST'])
def ediTranscript():
    datos = request.json
    file = datos.get('file')
    text = datos.get('text')
    if (file and text):
        [data, isError] = UserMusicController.editTranscript(file, text)
        return jsonify({ 'data': data , 'isError': isError}) , 200
    return jsonify({ 'data' : 'Ha ocurrido un error al guardar el texto', 'isError': True }) , 405

@app.route('/admin/transcript/list')
def list_transcript():
    try:
        [data, isError] = UserMusicController.listTrascript()
        return jsonify({'data': list(data), 'isError': isError}), 200
    except Exception as e:
        print(e)
        return jsonify({'data': 'Ha ocurrido un error', 'isError': True}), 500

@app.route('/admin/transcript/list/<string:file>')
def list_transcript_by_file(file):
    try:
        [data, isError] = UserMusicController.listTrascript(file)
        return jsonify({'data': list(data), 'isError': isError}), 200
    except Exception as e:
        print(e)
        return jsonify({'data': 'Ha ocurrido un error', 'isError': True}), 500

CORS(app)
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000,debug=True)
