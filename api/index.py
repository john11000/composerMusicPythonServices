import os
from serverComposer import Server
from flask import jsonify, request, send_file
from flask_cors import CORS
from controllers.auth import AuthController
from controllers.admin import UserMusicController
from pydub import AudioSegment
import pydub
AudioSegment.ffmpeg = "C:\\ffmpeg-6.0-essentials_build\\bin\\ffmpeg.exe"
AudioSegment.ffprobe = "C:\\ffmpeg-6.0-essentials_build\\bin\\ffprobe.exe"
import music21
# from api.controllers.mgen import MgenController
app = Server.getServer()
AuthController = AuthController()
UserMusicController = UserMusicController()
# MgenController = MgenController()

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
    print(datos)
    UserMusicController.GenerateMusic(datos=datos)
    return jsonify({ 'data' : list(UserMusicController.getListMusicGenerated()) }) , 200

@app.route('/admin/music/list/<string:token>')
def list_music(token):
    return jsonify({ 'data' : list(UserMusicController.getListMusicGenerated()) }) , 200


@app.route("/convert", methods=["POST"])
def convert():
  """Converts an MP3 file to a PDF of sheet music.

  Args:
    None.

  Returns:
    A PDF of sheet music.
  """

  # Get the MP3 file from the request.
  mp3_file = request.files["mp3_file"]

  # Extract the audio data from the MP3 file.
  audio_segment = pydub.AudioSegment.from_mp3(mp3_file)

  # Transcribe the audio data into sheet music notation.
  score = music21.converter.parse(audio_segment)

  # Export the sheet music notation to a PDF file.
  pdf_file = score.write("pdf", fp="output.pdf")

  # Return the PDF file to the client.
  return send_file(pdf_file, mimetype="application/pdf")


CORS(app)
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000,debug=True)
