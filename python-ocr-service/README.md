# Python OCR Service

OCR processing service for Daito Cards using PaddleOCR.

## Setup

1. Create virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Configure environment:
```bash
cp .env.example .env
# Edit .env with your settings
```

4. Run the service:
```bash
python server.py
```

## Docker

Build and run with Docker:
```bash
docker build -t daito-ocr-service .
docker run -p 5001:5001 --env-file .env daito-ocr-service
```

## API Endpoints

- `GET /health` - Health check
- `POST /api/ocr/process` - Process image for OCR

## Testing

Send a test request:
```bash
curl -X POST -F "image=@test_image.jpg" http://localhost:5001/api/ocr/process
```