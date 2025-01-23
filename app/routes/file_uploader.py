from functools import wraps
from flask import request, jsonify
import os
import uuid

def handle_file_upload(upload_folder='uploads', allowed_extensions=None):
    """
    Decorator to handle file uploads for Flask routes.
    
    Args:
        upload_folder (str): Directory where files will be saved.
        allowed_extensions (set): Set of allowed file extensions (e.g., {'pdf', 'png'}).
    
    Returns:
        function: Wrapped route function with file handling logic.
    """
    if allowed_extensions is None:
        allowed_extensions = {'pdf'}  # Default to only allow PDF files
    
    # Ensure the upload folder exists
    os.makedirs(upload_folder, exist_ok=True)
    
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            # Ensure 'file' exists in the request
            if 'file' not in request.files:
                return jsonify({"error": "No file part in the request"}), 400
            
            file = request.files['file']
            
            # Check if a file is selected
            if file.filename.strip() == '':
                return jsonify({"error": "No file selected for upload"}), 400
            
            # Validate file extension
            file_extension = file.filename.rsplit('.', 1)[-1].lower()
            if allowed_extensions and file_extension not in allowed_extensions:
                return jsonify({"error": f"Invalid file type. Allowed types: {', '.join(allowed_extensions)}"}), 400
            
            try:
                # Generate a unique file name to avoid conflicts
                unique_filename = f"{uuid.uuid4()}.{file_extension}"
                file_path = os.path.join(upload_folder, unique_filename)
                
                # Save the file
                file.save(file_path)
            except Exception as e:
                return jsonify({"error": "File upload failed", "details": str(e)}), 500
            
            # Pass file info to the wrapped function
            return func(*args, file_path=file_path, file_name=file.filename, **kwargs)
        
        return wrapper
    return decorator
