from flask import Flask, request, jsonify
import logging
from config import Config
from services.ollama_client import OllamaClient
from services.minio_client import MinioClient
from services.baserow_client import BaserowClient

app = Flask(__name__)
app.config.from_object(Config)

# Configuração básica de logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Initialize clients
ollama_client = OllamaClient(
    api_url=app.config['OLLAMA_API_URL']
)
minio_client = MinioClient(
    minio_url=app.config['MINIO_ENDPOINT'].replace('http://', ''), # MinIO client expects host:port
    access_key=app.config['MINIO_ROOT_USER'],
    secret_key=app.config['MINIO_ROOT_PASSWORD']
)
# O cliente Baserow será inicializado sob demanda, se as chaves estiverem presentes.
baserow_client = None
if app.config.get('BASEROW_API_KEY'):
    baserow_client = BaserowClient(
        base_url=app.config['BASEROW_ENDPOINT'],
        api_key=app.config['BASEROW_API_KEY']
    )

@app.route('/', methods=['GET'])
def index():
    return jsonify({
        "message": "nCA Toolkit is running.",
        "endpoints": ["/health", "/insight", "/upload", "/log"]
    }), 200

@app.route('/health', methods=['GET'])
def health():
    logging.info("Health check requested.")
    return jsonify({"status": "healthy"}), 200

@app.route('/insight', methods=['POST'])
def insight():
    data = request.json
    if not data or 'input' not in data:
        logging.warning("Insight request missing 'input' data.")
        return jsonify({"error": "Missing 'input' in request body"}), 400
    try:
        response = ollama_client.generate_response(data.get('input'))
        logging.info("Insight generated successfully.")
        return jsonify({"response": response}), 200
    except Exception as e:
        logging.error(f"Error generating insight: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/upload', methods=['POST'])
def upload():
    if 'file' not in request.files:
        logging.warning("Upload request missing 'file'.")
        return jsonify({"error": "No file part in the request"}), 400
    file = request.files['file']
    if file.filename == '':
        logging.warning("Upload request received empty filename.")
        return jsonify({"error": "No selected file"}), 400
    try:
        # Use the filename as object_name, or generate a unique one
        object_name = file.filename
        # MinIO client expects a file-like object, not a path
        result = minio_client.upload_file(bucket_name="nca-toolkit-uploads", file_object=file, object_name=object_name)
        logging.info(f"File '{object_name}' uploaded successfully to MinIO.")
        return jsonify(result), 201
    except Exception as e:
        logging.error(f"Error uploading file to MinIO: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/log', methods=['POST'])
def log():
    data = request.json
    table_id = app.config.get('BASEROW_TABLE_ID')

    if not baserow_client or not table_id:
        logging.error("BASEROW_TABLE_ID is not configured for logging.")
        return jsonify({"error": "Baserow client or table ID is not configured on the server."}), 500

    try:
        baserow_client.log_entry(table_id, data)
        logging.info("Log entry created successfully in Baserow.")
        return jsonify({"message": "Log entry created successfully"}), 201
    except Exception as e:
        logging.error(f"Error logging entry to Baserow: {e}")
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=app.config['NCA_TOOLKIT_PORT'])