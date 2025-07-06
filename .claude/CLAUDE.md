# Daito Cards - OCR Processing System

## Project Overview
A two-part application system for processing card images using OCR technology:
- **Part 1**: Laravel PHP client application (frontend/API)
- **Part 2**: Python OCR service (backend processing)

## Architecture

### System Flow
1. User uploads card image through Laravel web interface
2. Laravel validates and forwards image to Python OCR service
3. Python service processes image using OCR
4. OCR results returned to Laravel
5. Laravel displays results to user

### Technology Stack

#### Laravel Client (Part 1)
- Framework: Laravel (version 6.2)
- Frontend: Blade templates / Vue.js (TBD)
- Database: MySQL/PostgreSQL for storing OCR results
- Image handling: Laravel file uploads
- HTTP Client: Guzzle for API communication

#### Python OCR Service (Part 2)
- Framework: Flask
- OCR Engine: PaddleOCR (TBD)
- Image Processing: OpenCV, Pillow
- Package needed: ultralytics paddleocr paddlepaddle opencv-python
- API: REST endpoints for image processing
- Response Format: JSON
- Host by Docker with port 5001
## API Design

### Endpoints

#### Python OCR Service
- `POST /api/ocr/process` - Process single image
  - Request: multipart/form-data with image file
  - Response: JSON with extracted text and confidence scores

#### Laravel Client
- `GET /` - Homepage with upload form
- `POST /upload` - Handle image upload
- `GET /results/{id}` - View OCR results
- `GET /api/history` - User's OCR history

## Project Structure

```
daito-cards/
├── laravel-client/          # Laravel application
│   ├── app/
│   ├── resources/
│   ├── routes/
│   └── ...
├── python-ocr-service/      # Python OCR service
│   ├── server.py
│   ├── services/
│   ├── models/
│   └── requirements.txt
└── CLAUDE.md               # This file
```

## Development Guidelines

### Code Standards
- Laravel: PSR-12 coding standards
- Python: PEP 8 style guide
- API: RESTful conventions
- Git: Conventional commits

### Security Considerations
- Validate image uploads (file type, size)
- Sanitize OCR output before display
- Implement rate limiting
- Use HTTPS for production
- Store sensitive configs in .env files

### Testing
- Laravel: PHPUnit for unit/feature tests
- Python: pytest for service tests
- Integration tests for full flow

## Setup Instructions

### Laravel Client Setup
```bash
cd laravel-client
composer install
cp .env.example .env
php artisan key:generate
php artisan migrate
npm install && npm run dev
php artisan serve
```

### Python OCR Service Setup
```bash
cd python-ocr-service
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
python server.py
```

## Environment Variables

### Laravel (.env)
```
OCR_SERVICE_URL=http://localhost:5001
OCR_SERVICE_TIMEOUT=30
MAX_UPLOAD_SIZE=10M
```

### Python (.env)
```
PORT=5001
MAX_IMAGE_SIZE=10485760
OCR_ENGINE=paddleocr
ALLOWED_ORIGINS=http://localhost:8000,http://localhost:3000
```

## Common Tasks

### Adding New OCR Features
1. Update Python service with new processing logic
2. Add new API endpoint if needed
3. Update Laravel client to use new features
4. Add tests for both services

### Debugging OCR Issues
1. Check image quality and format
2. Review OCR service logs
3. Test with different OCR engines
4. Validate preprocessing steps

## Performance Considerations
- Implement image compression before sending to OCR
- Cache OCR results in Laravel
- Use queue system for async processing
- Consider horizontal scaling for OCR service

## Future Enhancements
- Batch processing support
- Multiple language OCR
- Real-time processing with WebSockets
- Mobile app integration
- OCR accuracy improvements with ML