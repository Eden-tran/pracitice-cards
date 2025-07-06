import cv2
import numpy as np
from paddleocr import PaddleOCR
from PIL import Image
import io
import logging
import base64
from .business_card_extractor import BusinessCardExtractor

class OCRService:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.ocr = PaddleOCR(
            use_angle_cls=True,
            lang='en'
        )
        self.extractor = BusinessCardExtractor()
    
    def process_image(self, image_file):
        try:
            image_bytes = image_file.read()
            image = Image.open(io.BytesIO(image_bytes))
            
            if image.mode != 'RGB':
                image = image.convert('RGB')
            
            img_array = np.array(image)
            
            preprocessed_img = self._preprocess_image(img_array)
            
            result = self.ocr.ocr(preprocessed_img, cls=True)
            
            extracted_data = self._parse_ocr_result(result)
            
            business_card_info = self.extractor.extract_info(extracted_data)
            
            return business_card_info
            
        except Exception as e:
            self.logger.error(f'Error in OCR processing: {str(e)}')
            raise
    
    def _preprocess_image(self, image):
        gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
        
        denoised = cv2.fastNlMeansDenoising(gray, None, 10, 7, 21)
        
        _, binary = cv2.threshold(denoised, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
        
        kernel = np.ones((1, 1), np.uint8)
        processed = cv2.morphologyEx(binary, cv2.MORPH_CLOSE, kernel)
        
        return cv2.cvtColor(processed, cv2.COLOR_GRAY2RGB)
    
    def _parse_ocr_result(self, result):
        extracted_data = []
        
        if not result or not result[0]:
            return extracted_data
        
        for line in result[0]:
            bbox = line[0]
            text = line[1][0]
            confidence = line[1][1]
            
            extracted_data.append({
                'text': text,
                'confidence': float(confidence),
                'bbox': {
                    'top_left': {'x': int(bbox[0][0]), 'y': int(bbox[0][1])},
                    'top_right': {'x': int(bbox[1][0]), 'y': int(bbox[1][1])},
                    'bottom_right': {'x': int(bbox[2][0]), 'y': int(bbox[2][1])},
                    'bottom_left': {'x': int(bbox[3][0]), 'y': int(bbox[3][1])}
                }
            })
        
        return extracted_data
    
    def _calculate_overall_confidence(self, text_blocks):
        if not text_blocks:
            return 0.0
        
        total_confidence = sum(block['confidence'] for block in text_blocks)
        return round(total_confidence / len(text_blocks), 4)