"""
Vercel Serverless Function for BPE AI Classification
"""
from http.server import BaseHTTPRequestHandler
import json
import sys
import os
from pathlib import Path

# Add parent directory to path to import modules
sys.path.insert(0, str(Path(__file__).parent.parent))

from worldList import type_of_word, ensure_nltk_data

class handler(BaseHTTPRequestHandler):
    def do_POST(self):
        try:
            # Initialize NLTK data
            ensure_nltk_data()
            
            # Get content length and read body
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            
            # Parse JSON
            data = json.loads(post_data.decode('utf-8'))
            labels = data.get('labels', [])
            
            # Classify labels
            result = self.classify_labels(labels)
            
            # Send response
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            
            self.wfile.write(json.dumps(result).encode())
            
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
    
    def classify_labels(self, labels):
        """Classify labels into categories based on first word type."""
        verb_phrases = []
        noun_phrases = []
        others = []
        skipped = []
        
        for label in labels:
            label = label.strip()
            
            if not label:
                continue
                
            words = label.split()
            if not words:
                skipped.append(label)
                continue
                
            first_word = words[0]
            word_type = type_of_word(first_word)
            
            if word_type == 'verb':
                verb_phrases.append({
                    'label': label,
                    'firstWord': first_word
                })
            elif word_type == 'noun':
                noun_phrases.append({
                    'label': label,
                    'firstWord': first_word
                })
            else:
                others.append({
                    'label': label,
                    'firstWord': first_word,
                    'wordType': word_type
                })
        
        total = len(verb_phrases) + len(noun_phrases) + len(others) + len(skipped)
        
        return {
            'verbPhrases': verb_phrases,
            'nounPhrases': noun_phrases,
            'others': others,
            'skipped': skipped,
            'statistics': {
                'total': total,
                'actionCount': len(verb_phrases),
                'objectCount': len(noun_phrases),
                'unclassifiedCount': len(others),
                'skippedCount': len(skipped)
            }
        }
