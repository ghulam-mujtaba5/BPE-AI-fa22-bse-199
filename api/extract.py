"""
Vercel Serverless Function for XML Label Extraction
"""
from http.server import BaseHTTPRequestHandler
import json
import sys
from pathlib import Path
import tempfile
import os

# Add parent directory to path to import modules
sys.path.insert(0, str(Path(__file__).parent.parent))

from xml_extractor import extract_labels_with_space

class handler(BaseHTTPRequestHandler):
    def do_POST(self):
        try:
            # Get content length and read body
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            
            # Parse JSON
            data = json.loads(post_data.decode('utf-8'))
            xml_content = data.get('xmlContent', '')
            
            if not xml_content:
                raise ValueError('No XML content provided')
            
            # Create temporary file to process XML
            with tempfile.NamedTemporaryFile(mode='w', suffix='.xml', delete=False) as tmp_file:
                tmp_file.write(xml_content)
                tmp_path = tmp_file.name
            
            try:
                # Extract labels
                labels = extract_labels_with_space(Path(tmp_path))
                
                # Send response
                self.send_response(200)
                self.send_header('Content-type', 'application/json')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                
                result = {
                    'labels': labels,
                    'count': len(labels)
                }
                
                self.wfile.write(json.dumps(result).encode())
            finally:
                # Clean up temp file
                os.unlink(tmp_path)
            
        except Exception as e:
            self.send_response(500)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            
            error_response = {
                'error': str(e),
                'type': type(e).__name__
            }
            self.wfile.write(json.dumps(error_response).encode())
    
    def do_OPTIONS(self):
        """Handle CORS preflight"""
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()
