@extends('layouts.app')

@section('content')
<div class="container">
    <div class="row justify-content-center">
        <div class="col-md-8">
            <div class="card">
                <div class="card-header">Business Card OCR Scanner</div>

                <div class="card-body">
                    <form id="uploadForm" enctype="multipart/form-data">
                        @csrf
                        <div class="form-group">
                            <label for="image">Select Business Card Image</label>
                            <input type="file" class="form-control-file" id="image" name="image" accept="image/*" required>
                            <small class="form-text text-muted">Supported formats: JPEG, PNG, JPG, GIF, BMP (Max: 10MB)</small>
                        </div>

                        <div class="form-group">
                            <img id="preview" src="#" alt="Preview" style="max-width: 100%; display: none;" class="mb-3">
                        </div>

                        <button type="submit" class="btn btn-primary">Upload and Process</button>
                    </form>

                    <div id="loading" class="text-center mt-4" style="display: none;">
                        <div class="spinner-border" role="status">
                            <span class="sr-only">Processing...</span>
                        </div>
                        <p>Processing your business card...</p>
                    </div>

                    <div id="results" class="mt-4" style="display: none;">
                        <h4>Extracted Information:</h4>
                        <table class="table">
                            <tbody>
                                <tr>
                                    <th>Name:</th>
                                    <td id="result-name"></td>
                                </tr>
                                <tr>
                                    <th>Title:</th>
                                    <td id="result-title"></td>
                                </tr>
                                <tr>
                                    <th>Company:</th>
                                    <td id="result-company"></td>
                                </tr>
                                <tr>
                                    <th>Email:</th>
                                    <td id="result-email"></td>
                                </tr>
                                <tr>
                                    <th>Phone:</th>
                                    <td id="result-phone"></td>
                                </tr>
                                <tr>
                                    <th>Website:</th>
                                    <td id="result-website"></td>
                                </tr>
                                <tr>
                                    <th>Address:</th>
                                    <td id="result-address"></td>
                                </tr>
                                <tr>
                                    <th>Confidence:</th>
                                    <td id="result-confidence"></td>
                                </tr>
                            </tbody>
                        </table>
                        
                        <div class="mt-3">
                            <h5>Raw Text:</h5>
                            <pre id="result-raw-text" class="border p-2 bg-light"></pre>
                        </div>
                    </div>

                    <div id="error" class="alert alert-danger mt-4" style="display: none;"></div>
                </div>
            </div>
        </div>
    </div>
</div>

<script>
    document.getElementById('image').addEventListener('change', function(e) {
        const file = e.target.files[0];
        if (file) {
            const reader = new FileReader();
            reader.onload = function(e) {
                document.getElementById('preview').src = e.target.result;
                document.getElementById('preview').style.display = 'block';
            };
            reader.readAsDataURL(file);
        }
    });

    document.getElementById('uploadForm').addEventListener('submit', function(e) {
        e.preventDefault();
        
        const formData = new FormData();
        const fileInput = document.getElementById('image');
        formData.append('image', fileInput.files[0]);
        formData.append('_token', '{{ csrf_token() }}');

        // Hide previous results and errors
        document.getElementById('results').style.display = 'none';
        document.getElementById('error').style.display = 'none';
        document.getElementById('loading').style.display = 'block';

        fetch('/upload', {
            method: 'POST',
            body: formData
        })
        .then(response => response.json())
        .then(data => {
            document.getElementById('loading').style.display = 'none';
            
            if (data.success) {
                // Display results
                document.getElementById('result-name').textContent = data.data.name || '-';
                document.getElementById('result-title').textContent = data.data.title || '-';
                document.getElementById('result-company').textContent = data.data.company || '-';
                document.getElementById('result-email').textContent = data.data.email || '-';
                document.getElementById('result-phone').textContent = data.data.phone || '-';
                document.getElementById('result-website').textContent = data.data.website || '-';
                document.getElementById('result-address').textContent = data.data.address || '-';
                document.getElementById('result-confidence').textContent = 
                    data.data.confidence ? (data.data.confidence * 100).toFixed(2) + '%' : '-';
                document.getElementById('result-raw-text').textContent = data.data.raw_text || '';
                
                document.getElementById('results').style.display = 'block';
            } else {
                document.getElementById('error').textContent = data.message || 'An error occurred';
                document.getElementById('error').style.display = 'block';
            }
        })
        .catch(error => {
            document.getElementById('loading').style.display = 'none';
            document.getElementById('error').textContent = 'Network error: ' + error.message;
            document.getElementById('error').style.display = 'block';
        });
    });
</script>
@endsection