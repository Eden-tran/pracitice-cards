#!/usr/bin/env python3
import requests
import sys

def test_ocr_service():
    url = "http://localhost:5001/health"
    
    print("Testing OCR Service Health Check...")
    try:
        response = requests.get(url)
        if response.status_code == 200:
            print(f"✓ Health check passed: {response.json()}")
        else:
            print(f"✗ Health check failed: {response.status_code}")
    except Exception as e:
        print(f"✗ Could not connect to OCR service: {e}")
        print("Make sure the service is running on port 5001")
        
    print("\nTo test image processing:")
    print("curl -X POST -F 'image=@test_image.jpg' http://localhost:5001/api/ocr/process")

if __name__ == "__main__":
    test_ocr_service()