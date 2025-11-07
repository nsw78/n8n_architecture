from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

class Config:
    # General configuration
    DEBUG = os.getenv("DEBUG", "False") == "True"
    ENV = os.getenv("ENV", "development")
    SECRET_KEY = os.getenv("SECRET_KEY", "your_secret_key")

    # n8n configuration
    N8N_PORT = os.getenv("N8N_PORT", 5678)
    N8N_BASIC_AUTH_ACTIVE = os.getenv("N8N_BASIC_AUTH_ACTIVE", "false") == "true"
    N8N_BASIC_AUTH_USER = os.getenv("N8N_BASIC_AUTH_USER", "admin")
    N8N_BASIC_AUTH_PASSWORD = os.getenv("N8N_BASIC_AUTH_PASSWORD", "admin123")
    N8N_ENCRYPTION_KEY = os.getenv("N8N_ENCRYPTION_KEY", "supersecreta")

    # MinIO configuration
    MINIO_ROOT_USER = os.getenv("MINIO_ROOT_USER", "admin")
    MINIO_ROOT_PASSWORD = os.getenv("MINIO_ROOT_PASSWORD", "admin123")    
    MINIO_ENDPOINT = os.getenv("MINIO_ENDPOINT", "minio:9000")

    # Baserow configuration
    BASEROW_PORT = os.getenv("BASEROW_PORT", 8000)
    BASEROW_PUBLIC_URL = os.getenv("BASEROW_PUBLIC_URL", "http://localhost:8000")
    BASEROW_API_KEY = os.getenv("BASEROW_API_KEY")
    BASEROW_ENDPOINT = os.getenv("BASEROW_ENDPOINT", "http://baserow:80")

    # Kokoro TTS configuration
    KOKORO_PORT = os.getenv("KOKORO_PORT", 5002)
    KOKORO_ENDPOINT = os.getenv("KOKORO_ENDPOINT", "http://kokoro:5002")

    # NCA Toolkit configuration
    NCA_TOOLKIT_KEY = os.getenv("NCA_TOOLKIT_KEY", "nca-key-12345")
    NCA_TOOLKIT_PORT = os.getenv("NCA_TOOLKIT_PORT", 8088)

    # Ollama configuration
    OLLAMA_API_URL = os.getenv("OLLAMA_API_URL", "http://ollama:11434")