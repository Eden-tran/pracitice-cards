<?php

namespace App\Http\Controllers;

use Illuminate\Http\Request;
use GuzzleHttp\Client;
use GuzzleHttp\Exception\RequestException;

class BusinessCardController extends Controller
{
    protected $httpClient;
    protected $ocrServiceUrl;

    public function __construct()
    {
        $this->httpClient = new Client([
            'timeout' => env('OCR_SERVICE_TIMEOUT', 30),
        ]);
        $this->ocrServiceUrl = env('OCR_SERVICE_URL', 'http://localhost:5001');
    }

    public function index()
    {
        return view('business-cards.index');
    }

    public function upload(Request $request)
    {
        $request->validate([
            'image' => 'required|image|mimes:jpeg,png,jpg,gif,bmp|max:10240', // 10MB max
        ]);

        try {
            $image = $request->file('image');
            
            // Send image to OCR service
            $response = $this->httpClient->post($this->ocrServiceUrl . '/api/ocr/process', [
                'multipart' => [
                    [
                        'name' => 'image',
                        'contents' => fopen($image->getPathname(), 'r'),
                        'filename' => $image->getClientOriginalName()
                    ]
                ]
            ]);

            $result = json_decode($response->getBody(), true);

            if (isset($result['status']) && $result['status'] === 'success') {
                // Save to database if needed
                $this->saveBusinessCard($result['data']);
                
                return response()->json([
                    'success' => true,
                    'data' => $result['data'],
                    'message' => 'OCR processing completed successfully'
                ]);
            }

            return response()->json([
                'success' => false,
                'message' => 'OCR processing failed'
            ], 500);

        } catch (RequestException $e) {
            return response()->json([
                'success' => false,
                'message' => 'Failed to connect to OCR service: ' . $e->getMessage()
            ], 500);
        } catch (\Exception $e) {
            return response()->json([
                'success' => false,
                'message' => 'An error occurred: ' . $e->getMessage()
            ], 500);
        }
    }

    public function results($id)
    {
        // Retrieve from database
        // For now, we'll just show a view
        return view('business-cards.results', compact('id'));
    }

    public function history()
    {
        // Get user's OCR history from database
        // For now, return empty array
        $history = [];
        
        return response()->json([
            'success' => true,
            'data' => $history
        ]);
    }

    private function saveBusinessCard($data)
    {
        // TODO: Save to database
        // This would create a BusinessCard model entry
        // For now, we'll skip database storage
    }
}
