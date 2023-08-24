from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/')
def home():
    return jsonify({ 'version': '0.0.1', 'description': 'Servicio python composer music'  })

@app.route('/about')
def about():
    return 'About'