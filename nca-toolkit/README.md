# nCA Toolkit

## Overview
The nCA Toolkit is a Flask-based application designed to provide a set of services for AI responses, file uploads, and logging. It integrates with various services such as Ollama for AI responses, MinIO for object storage, and Baserow for logging data.

## Project Structure
```
nca-toolkit
├── src
│   ├── main.py                # Entry point of the Flask application
│   ├── config.py              # Configuration settings
│   ├── services                # Service clients for external integrations
│   │   ├── ollama_client.py    # Client for Ollama AI service
│   │   ├── minio_client.py     # Client for MinIO object storage
│   │   └── baserow_client.py   # Client for Baserow database
│   └── utils                  # Utility functions
│       └── logger.py          # Logger setup
├── tests                       # Unit tests for the application
│   └── test_main.py           # Tests for main application endpoints
├── requirements.txt            # Project dependencies
├── Dockerfile                  # Docker image setup
├── docker-compose.yml          # Service orchestration
├── .env                        # Environment variables
├── .gitignore                  # Git ignore rules
└── README.md                   # Project documentation
```

## Setup Instructions
1. Clone the repository:
   ```
   git clone <repository-url>
   cd nca-toolkit
   ```

2. Create a virtual environment and activate it:
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

4. Configure environment variables in the `.env` file as needed.

5. Run the application:
   ```
   python src/main.py
   ```

## Usage
- **Health Check**: Access the `/health` endpoint to check the status of the application.
- **Generate Insight**: Use the `/insight` endpoint to generate AI responses.
- **File Upload**: Send files to the `/upload` endpoint to store them in MinIO.
- **Log Entry**: Use the `/log` endpoint to log data to Baserow.

## Docker
To run the application using Docker, use the following command:
```
docker-compose up
```

## Contributing
Contributions are welcome! Please submit a pull request or open an issue for any enhancements or bug fixes.

## License
This project is licensed under the MIT License. See the LICENSE file for details.