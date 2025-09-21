#!/usr/bin/env python3
"""
JollyLLBot Chat Prototype
Simple Flask app to serve the chat interface prototype
"""

import os
import sys
from flask import Flask, render_template, jsonify, request

# Add parent directory to path to import from src
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.whatsapp_bot import WhatsAppBot

app = Flask(__name__, 
           template_folder='templates',
           static_folder='static')

# Initialize WhatsApp bot for message processing
whatsapp_bot = WhatsAppBot()

@app.route('/')
def chat():
    """Serve the chat interface"""
    return render_template('chat.html')

@app.route('/api/chat', methods=['POST'])
def chat_api():
    """API endpoint for chat messages"""
    try:
        data = request.get_json()
        message = data.get('message', '').strip().lower()
        
        if not message:
            return jsonify({'error': 'No message provided'}), 400
        
        # Process message using WhatsApp bot logic
        if message in ['hello', 'hi', 'start', 'help']:
            response = whatsapp_bot._get_welcome_message()
        elif 'analyze' in message or 'document' in message:
            response = whatsapp_bot._get_document_instructions()
        elif 'status' in message:
            response = whatsapp_bot._get_status_message()
        else:
            response = whatsapp_bot._get_default_message()
        
        return jsonify({'response': response})
        
    except Exception as e:
        return jsonify({'error': 'Sorry, I encountered an error. Please try again later.'}), 500

@app.route('/health')
def health():
    """Health check endpoint"""
    return jsonify({'status': 'healthy', 'service': 'JollyLLBot Chat Prototype'})

if __name__ == '__main__':
    port = int(os.getenv('PORT', 8080))
    print(f"Starting JollyLLBot Chat Prototype on port {port}")
    app.run(host='0.0.0.0', port=port, debug=True)