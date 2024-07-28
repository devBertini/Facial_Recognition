import os
from flask import Flask
from routes.upload import upload_bp
from routes.recognize import recognize_bp

app = Flask(__name__)

#Registra Blueprints
app.register_blueprint(upload_bp)
app.register_blueprint(recognize_bp)

if __name__ == '__main__':
    host = os.getenv('FLASK_RUN_HOST', '0.0.0.0')
    port = int(os.getenv('FLASK_RUN_PORT', 5000))
    app.run(host=host, port=port)
