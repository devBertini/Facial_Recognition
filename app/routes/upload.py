from flask import Blueprint, request, jsonify
from db import get_db_connection
import pymysql
import pymysql.cursors
import face_recognition
import io

upload_bp = Blueprint('upload', __name__)

@upload_bp.route('/upload', methods=['POST'])
def upload():
    if 'file' not in request.files:
        return jsonify({'error': 'Nenhum arquivo de imagem encontrado.'}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'Uma imagem não foi enviada na requisição.'}), 400

    name = request.form.get('name')
    registration = request.form.get('registration')
    cpf = request.form.get('cpf')

    if not all([name, registration, cpf, file]):
        return jsonify({'error': 'Um ou mais campos não foram enviados na solicitação.'}), 400

    #Lê a imagem em bytes
    image_bytes = file.read()
    
    #Carrega a imagem e converte para RGB
    image = face_recognition.load_image_file(io.BytesIO(image_bytes))

    #Detecta e codifica o rosto na imagem
    face_encodings = face_recognition.face_encodings(image)
    if not face_encodings:
        return jsonify({'error': 'Não foi encontrado um rosto na imagem.'}), 400

    #Obtem a primeira codificação de rosto (assumindo uma única face por imagem)
    face_encoding = face_encodings[0]

    #Conectar ao banco e salva as informações
    connection = get_db_connection()
    try:
        with connection.cursor() as cursor:
            #Inseri ou atualizar o colaborador
            cursor.execute(
                "INSERT INTO collaborators (name, registration, cpf) VALUES (%s, %s, %s) ON DUPLICATE KEY UPDATE name=VALUES(name), registration=VALUES(registration), cpf=VALUES(cpf)",
                (name, registration, cpf)
            )
            collaborator_id = cursor.lastrowid

            #Inseri a imagem e a codificação facial
            cursor.execute(
                "INSERT INTO face_images (collaborator_id, image, face_encoding) VALUES (%s, %s, %s)",
                (collaborator_id, image_bytes, str(face_encoding.tolist()))
            )
            connection.commit()
    finally:
        connection.close()

    return jsonify({'message': 'Colaborador cadastrado com sucesso!'}), 200
