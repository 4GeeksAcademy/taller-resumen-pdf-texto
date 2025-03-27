"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
from flask import Flask, request, jsonify, url_for, Blueprint, current_app
from api.models import db, User
from api.utils import generate_sitemap, APIException
from flask_cors import CORS
import os
import fitz  # PyMuPDF
from .chatgpt_service import summarize_text, extract_text_from_pdf
from werkzeug.utils import secure_filename

api = Blueprint('api', __name__)

# Allow CORS requests to this API
CORS(api)


@api.route('/hello', methods=['POST', 'GET'])
def handle_hello():

    response_body = {
        "message": "Hello! I'm a message that came from the backend, check the network tab on the google inspector and you will see the GET request"
    }

    return jsonify(response_body), 200

@api.route("/upload", methods=["POST"])
def upload_file():
    text = None

    # Verificar si se envió un archivo
    if 'file' in request.files:
        file = request.files['file']
        if file.filename == '' or not file.filename.endswith(('.pdf', '.txt')):
            return jsonify({"error": "Nombre de archivo inválido o formato no soportado"}), 400
        
        filename = secure_filename(file.filename)
        file_path = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)
        # Extraer texto del archivo PDF o TXT
        if filename.endswith(".pdf"):
            text = extract_text_from_pdf(file_path)
        elif filename.endswith(".txt"):
            with open(file_path, "r", encoding="utf-8") as f:
                text = f.read()
    # Verificar si se envió texto directamente
    elif 'text' in request.form:
        text = request.form['text']
        if not text.strip():
            return jsonify({"error": "El texto proporcionado está vacío"}), 400
    else:
        return jsonify({"error": "No se proporcionó texto ni archivo"}), 400

    # Generar el resumen
    summary = summarize_text(text)
    return jsonify({"summary": summary})