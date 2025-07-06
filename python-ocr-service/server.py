from flask import Flask, request, jsonify
from flask_cors import CORS
import os
from dotenv import load_dotenv
from services.ocr_service import OCRService
from config.settings import Config
from config.logging_config import setup_logging

load_dotenv()

app = Flask(__name__)
app.config.from_object(Config)
Config.init_app(app)
setup_logging(app)
CORS(app, origins=app.config['ALLOWED_ORIGINS'])

ocr_service = OCRService()

@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({'status': 'healthy', 'service': 'OCR Service'}), 200

@app.route('/api/ocr/process', methods=['POST'])
def process_image():
    try:
        if 'image' not in request.files:
            return jsonify({'error': 'No image file provided'}), 400
        
        file = request.files['image']
        
        if file.filename == '':
            return jsonify({'error': 'No image selected'}), 400
        
        if not allowed_file(file.filename):
            return jsonify({'error': 'Invalid file type. Allowed types: png, jpg, jpeg, gif, bmp'}), 400
        
        if file.content_length > app.config['MAX_IMAGE_SIZE']:
            return jsonify({'error': 'File size exceeds maximum allowed size'}), 400
        
        result = ocr_service.process_image(file)
        
        return jsonify({
            'status': 'success',
            'data': result
        }), 200
        
    except Exception as e:
        app.logger.error(f'Error processing image: {str(e)}')
        return jsonify({'error': 'Internal server error'}), 500

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Not found'}), 404

@app.errorhandler(500)
def internal_error(error):
    app.logger.error(f'Internal error: {str(error)}')
    return jsonify({'error': 'Internal server error'}), 500

@app.errorhandler(413)
def request_entity_too_large(error):
    return jsonify({'error': 'File too large'}), 413

if __name__ == '__main__':
    port = int(os.getenv('PORT', 5001))
    app.run(host='0.0.0.0', port=port, debug=app.config['DEBUG'])