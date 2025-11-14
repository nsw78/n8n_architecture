from flask import Flask, request, jsonify
import logging
import json
import requests
import tempfile
from moviepy.editor import ImageClip, AudioFileClip, CompositeVideoClip
from config import Config
from services.ollama_client import OllamaClient
import os
from services.minio_client import MinioClient
from services.baserow_client import BaserowClient

app = Flask(__name__)
app.config.from_object(Config)

# Configuração básica de logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

@app.route('/', methods=['GET'])
def index():
    return jsonify({
        "message": "nCA Toolkit is running.",
        "endpoints": ["/health", "/insight", "/upload", "/log", "/data/timeline", "/render"]
    }), 200

@app.route('/health', methods=['GET'])
def health():
    logging.info("Health check requested.")
    return jsonify({"status": "healthy"}), 200

@app.route('/insight', methods=['GET', 'POST'])
def insight():
    prompt = None
    if request.method == 'POST':
        data = request.json
        if not data or 'input' not in data:
            logging.warning("Insight POST request missing 'input' data.")
            return jsonify({"error": "Missing 'input' in request body"}), 400
        prompt = data.get('input')
    else:  # GET request
        prompt = request.args.get('input')
        if not prompt:
            logging.warning("Insight GET request missing 'input' parameter.")
            return jsonify({"error": "Missing 'input' query parameter"}), 400

    try:
        # Inicialização Tardia do Cliente
        ollama_client = OllamaClient(api_url=app.config.get('OLLAMA_API_URL'))
        response = ollama_client.generate_response(prompt)
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
        # Inicialização Tardia do Cliente
        minio_client = MinioClient(
            minio_url=app.config.get('MINIO_ENDPOINT'),
            access_key=app.config.get('MINIO_ROOT_USER'),
            secret_key=app.config.get('MINIO_ROOT_PASSWORD')
        )

        object_name = file.filename
        result = minio_client.upload_file(
            bucket_name="nca-toolkit-uploads",
            object_name=object_name,
            data_stream=file.stream,
            data_length=file.content_length,
            content_type=file.content_type
        )
        logging.info(f"File '{object_name}' uploaded successfully to MinIO.")
        return jsonify(result), 201
    except Exception as e:
        logging.error(f"Error uploading file to MinIO: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/log', methods=['POST'])
def log():
    data = request.json
    table_id = app.config.get('BASEROW_TABLE_ID')
    api_key = app.config.get('BASEROW_API_KEY')

    if not api_key or not table_id:
        logging.error("BASEROW_API_KEY or BASEROW_TABLE_ID is not configured for logging.")
        return jsonify({"error": "Baserow client or table ID is not configured on the server."}), 500

    try:
        # Inicialização Tardia do Cliente
        baserow_client = BaserowClient(
            base_url=app.config.get('BASEROW_ENDPOINT'),
            api_key=api_key
        )
        baserow_client.log_entry(table_id, data)
        logging.info("Log entry created successfully in Baserow.")
        return jsonify({"message": "Log entry created successfully"}), 201
    except Exception as e:
        logging.error(f"Error logging entry to Baserow: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/render', methods=['POST'])
def render_video():
    """
    Endpoint para renderizar um vídeo a partir de uma imagem e um texto.
    Espera um JSON com 'image_url' e 'text'.
    """
    data = request.json
    if not data or 'image_url' not in data or 'text' not in data:
        logging.warning("Render request missing 'image_url' or 'text'.")
        return jsonify({"error": "Missing 'image_url' or 'text' in request body"}), 400

    image_url = data['image_url']
    text = data['text']
    video_filename = f"video_{tempfile._get_candidate_names()}.mp4"

    audio_file, image_file, video_file = None, None, None
    try:
        # 1. Gerar áudio com Kokoro
        logging.info("Requesting audio from Kokoro TTS...")
        kokoro_endpoint = app.config['KOKORO_ENDPOINT']
        tts_response = requests.post(kokoro_endpoint, json={"text": text})
        tts_response.raise_for_status()
        audio_content = tts_response.content

        # 2. Baixar a imagem
        logging.info(f"Downloading image from {image_url}...")
        image_response = requests.get(image_url)
        image_response.raise_for_status()
        image_content = image_response.content

        # 3. Criar arquivos temporários
        audio_file = tempfile.NamedTemporaryFile(delete=False, suffix=".wav")
        image_file = tempfile.NamedTemporaryFile(delete=False, suffix=".png")
        video_file = tempfile.NamedTemporaryFile(delete=False, suffix=".mp4")

        audio_file.write(audio_content)
        image_file.write(image_content)
        audio_file.close()
        image_file.close()

        # 4. Criar vídeo com MoviePy
        audio_clip = AudioFileClip(audio_file.name)
        image_clip = ImageClip(image_file.name).set_duration(audio_clip.duration)
        image_clip.fps = 24

        final_clip = image_clip.set_audio(audio_clip)
        logging.info("Rendering video file...")
        final_clip.write_videofile(video_file.name, codec='libx264', audio_codec='aac')

        # 5. Fazer upload do vídeo para o MinIO
        logging.info(f"Uploading video '{video_filename}' to MinIO...")
        minio_client = MinioClient(
            minio_url=app.config.get('MINIO_ENDPOINT'),
            access_key=app.config.get('MINIO_ROOT_USER'),
            secret_key=app.config.get('MINIO_ROOT_PASSWORD')
        )

        with open(video_file.name, 'rb') as f:
            file_size = os.path.getsize(video_file.name)
            result = minio_client.upload_file(
                bucket_name="nca-toolkit-uploads",
                object_name=video_filename,
                data_stream=f,
                data_length=file_size,
                content_type='video/mp4'
            )

        logging.info("Video rendered and uploaded successfully.")
        return jsonify(result), 201

    except Exception as e:
        logging.error(f"Error during video rendering: {e}")
        return jsonify({"error": str(e)}), 500
    finally:
        # Garante a limpeza dos arquivos temporários
        if audio_file:
            os.remove(audio_file.name)
        if image_file:
            os.remove(image_file.name)
        if video_file:
            os.remove(video_file.name)

@app.route('/data/timeline', methods=['GET'])
def get_timeline_data():
    try:
        # O caminho é relativo à raiz do projeto Docker, não ao nca-toolkit
        with open('/app/data/a_luz_nas_trevas.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
        logging.info("Timeline data loaded and returned successfully.")
        return jsonify(data.get("timeline", [])), 200
    except FileNotFoundError:
        logging.error("Data file 'a_luz_nas_trevas.json' not found.")
        return jsonify({"error": "Data file not found on server."}), 404
    except Exception as e:
        logging.error(f"Error reading data file: {e}")
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=app.config.get('NCA_TOOLKIT_PORT', 8088))