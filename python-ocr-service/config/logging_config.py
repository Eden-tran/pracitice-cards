import logging
import logging.handlers
import os

def setup_logging(app):
    log_level = os.getenv('LOG_LEVEL', 'INFO')
    log_format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    
    logging.basicConfig(
        level=getattr(logging, log_level.upper()),
        format=log_format
    )
    
    if not os.path.exists('logs'):
        os.makedirs('logs')
    
    file_handler = logging.handlers.RotatingFileHandler(
        'logs/ocr_service.log',
        maxBytes=10485760,  # 10MB
        backupCount=10
    )
    file_handler.setFormatter(logging.Formatter(log_format))
    file_handler.setLevel(logging.INFO)
    
    app.logger.addHandler(file_handler)
    app.logger.setLevel(logging.INFO)
    app.logger.info('OCR Service startup')