#!/usr/bin/env python3
"""
JollyLLBot - Legal Document Analysis AI Webapp/WhatsApp Bot
Main Flask application entry point
"""

import os
import logging
from flask import Flask, request, render_template, flash, redirect, url_for, jsonify
from werkzeug.utils import secure_filename
from dotenv import load_dotenv

from src.document_analyzer import DocumentAnalyzer
from src.whatsapp_bot import WhatsAppBot
from src.utils import allowed_file, setup_logging

# Load environment variables
load_dotenv()

# Setup logging
setup_logging()
logger = logging.getLogger(__name__)

# Initialize Flask app
app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('FLASK_SECRET_KEY', 'dev-secret-key')
app.config['MAX_CONTENT_LENGTH'] = int(os.getenv('MAX_FILE_SIZE_MB', 10)) * 1024 * 1024

# Initialize services
document_analyzer = DocumentAnalyzer()
whatsapp_bot = WhatsAppBot()

# Create upload directory
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


@app.route('/')
def index():
    """Main page with document upload form"""
    return render_template('index.html')


@app.route('/upload', methods=['POST'])
def upload_file():
    """Handle document upload and analysis"""
    try:
        if 'file' not in request.files:
            flash('No file selected')
            return redirect(request.url)
        
        file = request.files['file']
        if file.filename == '':
            flash('No file selected')
            return redirect(request.url)
        
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)
            
            # Analyze document
            analysis_result = document_analyzer.analyze_document(filepath)
            
            # Clean up uploaded file
            os.remove(filepath)
            
            return render_template('result.html', 
                                 filename=filename, 
                                 analysis=analysis_result)
        else:
            flash('Invalid file type. Please upload PDF, DOCX, or TXT files.')
            return redirect(request.url)
            
    except Exception as e:
        logger.error(f"Error processing upload: {str(e)}")
        flash('An error occurred while processing your document.')
        return redirect(url_for('index'))


@app.route('/api/analyze', methods=['POST'])
def api_analyze():
    """API endpoint for document analysis"""
    try:
        if 'file' not in request.files:
            return jsonify({'error': 'No file provided'}), 400
        
        file = request.files['file']
        if not allowed_file(file.filename):
            return jsonify({'error': 'Invalid file type'}), 400
        
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        
        # Analyze document
        analysis_result = document_analyzer.analyze_document(filepath)
        
        # Clean up uploaded file
        os.remove(filepath)
        
        return jsonify({
            'filename': filename,
            'analysis': analysis_result
        })
        
    except Exception as e:
        logger.error(f"API error: {str(e)}")
        return jsonify({'error': 'Analysis failed'}), 500


@app.route('/webhook/whatsapp', methods=['POST'])
def whatsapp_webhook():
    """WhatsApp webhook endpoint"""
    try:
        return whatsapp_bot.handle_message(request)
    except Exception as e:
        logger.error(f"WhatsApp webhook error: {str(e)}")
        return "OK", 200


@app.route('/health')
def health_check():
    """Health check endpoint"""
    return jsonify({'status': 'healthy', 'service': 'JollyLLBot'})


if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    debug = os.getenv('FLASK_ENV') == 'development'
    
    logger.info(f"Starting JollyLLBot on port {port}")
    app.run(host='0.0.0.0', port=port, debug=debug)