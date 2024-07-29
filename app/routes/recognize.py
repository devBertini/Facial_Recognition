from flask import Blueprint, request, jsonify
from utils.db_connection import get_db_connection
import pymysql.cursors
import face_recognition
import numpy as np
import hashlib
import pymysql
import ast
import os
import io

recognize_bp = Blueprint('recognize', __name__)

@recognize_bp.route('/recognize', methods=['POST'])
def recognize():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'Nenhum arquivo de imagem enviado.'}), 400

    #Lê a imagem em bytes
    image_bytes = file.read()

    #Carrega a imagem e converte para RGB
    image = face_recognition.load_image_file(io.BytesIO(image_bytes))
    
    #Detecta e codificar o rosto na imagem
    face_encodings = face_recognition.face_encodings(image)
    if not face_encodings:
        return jsonify({'error': 'Não foi identificado um rosto na imagem.'}), 400

    #Obtem a primeira codificação de rosto (assumindo uma única face por imagem)
    unknown_face_encoding = face_encodings[0]

    #Conecta ao banco e buscar codificações faciais
    connection = get_db_connection()
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT f.collaborator_id, c.name, registration, f.face_encoding FROM face_images f JOIN collaborators c ON f.collaborator_id = c.id")
            face_images = cursor.fetchall()
    finally:
        connection.close()

    if not face_images:
        return jsonify({'error': 'Não foi identificado rosto na imagem.'}), 404

    #Inicializa variáveis para armazenar o resultado
    best_match = None
    highest_similarity = 0

    #Comparar a codificação da imagem com as codificações dos colaboradores
    for face_image in face_images:
        stored_face_encoding = ast.literal_eval(face_image['face_encoding'])
        stored_face_encoding = np.array(stored_face_encoding)
        
        #Compara a codificação da imagem com a codificação armazenada
        distances = face_recognition.face_distance([stored_face_encoding], unknown_face_encoding)
        similarity = 1 - distances[0]  # Converte distância em similaridade
        
        #Atualiza a melhor correspondência se necessário
        if similarity > highest_similarity:
            highest_similarity = similarity
            best_match = face_image

    #Obtem o valor do limiar de similaridade a partir da variável de ambiente docker
    similarity_threshold = float(os.getenv('MINIMUM_SIMILARITY_THRESHOLD', '0.49'))

    #Verificar se a melhor correspondência tem confiança suficiente
    if highest_similarity >= similarity_threshold and best_match:
        #Verifica e remove imagens antigas se o colaborador já tem 10 imagens
        connection = get_db_connection()
        try:
            with connection.cursor() as cursor:
                cursor.execute(
                    "SELECT COUNT(*) as count FROM face_images WHERE collaborator_id = %s",
                    (best_match['collaborator_id'],)
                )
                result = cursor.fetchone()
                image_count = result['count']

                if image_count >= 10:
                    #Remover a imagem mais antiga armazenada
                    cursor.execute(
                        "DELETE FROM face_images WHERE id = (SELECT id FROM face_images WHERE collaborator_id = %s ORDER BY id ASC LIMIT 1)",
                        (best_match['collaborator_id'],)
                    )

                #Verificar se a imagem já está armazenada
                image_hash = hashlib.md5(image_bytes).hexdigest()
                cursor.execute(
                    "SELECT COUNT(*) as count FROM face_images WHERE collaborator_id = %s AND MD5(image) = %s",
                    (best_match['collaborator_id'], image_hash)
                )
                result = cursor.fetchone()
                image_exists = result['count'] > 0

                if not image_exists:
                    #Insere a nova imagem e codificação facial
                    cursor.execute(
                        "INSERT INTO face_images (collaborator_id, image, face_encoding) VALUES (%s, %s, %s)",
                        (best_match['collaborator_id'], image_bytes, str(unknown_face_encoding.tolist()))
                    )
                    connection.commit()
        finally:
            connection.close()

        return jsonify({
            'name': best_match['name'],
            'registration': best_match['registration'],
            'similarity': highest_similarity
        }), 200

    return jsonify({'message': 'Não foi encontrato nenhuma pessoa correspondente a da imagem.'}), 404
