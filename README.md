# JollyLLBot - Legal Document Analysis AI

A prototype AI-powered legal document analysis assistant that provides web interface and WhatsApp bot functionality for analyzing legal documents.

## Features

🏛️ **Legal Document Analysis**
- Upload PDF, DOCX, and TXT files
- AI-powered document analysis using OpenAI GPT
- Extract key points and legal insights
- Identify potential risks and concerns
- Generate actionable recommendations

📱 **Multi-Platform Access**
- Modern responsive web interface
- WhatsApp bot integration via Twilio
- RESTful API for third-party integrations

🧠 **AI-Powered Insights**
- Document type identification
- Legal risk assessment  
- Key clause extraction
- Professional recommendations
- Comprehensive document summaries

## Quick Start

### Prerequisites
- Python 3.8+
- OpenAI API key (optional - will use mock analysis without it)
- Twilio account (optional - for WhatsApp bot functionality)

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd JollyLLBot-
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure environment variables**
   ```bash
   cp .env.example .env
   # Edit .env with your API keys and configuration
   ```

4. **Run the application**
   ```bash
   python app.py
   ```

5. **Access the web interface**
   - Open http://localhost:5000 in your browser
   - Upload a legal document for analysis

## Configuration

### Environment Variables

Create a `.env` file with the following variables:

```env
# OpenAI Configuration (Optional)
OPENAI_API_KEY=your_openai_api_key_here

# Twilio Configuration for WhatsApp (Optional)
TWILIO_ACCOUNT_SID=your_twilio_account_sid
TWILIO_AUTH_TOKEN=your_twilio_auth_token
TWILIO_WHATSAPP_NUMBER=whatsapp:+14155238886

# Flask Configuration
FLASK_SECRET_KEY=your_secret_key_here
FLASK_ENV=development

# Upload Configuration
MAX_FILE_SIZE_MB=10
ALLOWED_EXTENSIONS=pdf,docx,txt
```

### Supported File Types
- **PDF**: Portable Document Format files
- **DOCX**: Microsoft Word documents
- **TXT**: Plain text files

### File Size Limits
- Maximum file size: 10MB (configurable)
- Recommended for optimal performance: Under 5MB

## API Endpoints

### Web Interface
- `GET /` - Main upload page
- `POST /upload` - Document upload and analysis
- `GET /health` - System health check

### API Endpoints
- `POST /api/analyze` - Programmatic document analysis
- `POST /webhook/whatsapp` - WhatsApp webhook endpoint

### Example API Usage

```bash
curl -X POST -F "file=@contract.pdf" \
     http://localhost:5000/api/analyze
```

Response:
```json
{
  "filename": "contract.pdf",
  "analysis": {
    "summary": "Commercial lease agreement...",
    "key_points": ["Rent: $2000/month", "Term: 2 years"],
    "document_type": "Lease Agreement",  
    "risks_concerns": ["Early termination clause"],
    "recommendations": ["Review termination terms"]
  }
}
```

## WhatsApp Bot Commands

Send these messages to your configured WhatsApp bot:

- `hello` or `hi` - Welcome message and instructions
- `analyze` - Get document analysis instructions
- `status` - Check system status
- `help` - Show available commands

## Architecture

```
JollyLLBot/
├── app.py                 # Flask application entry point
├── src/
│   ├── document_analyzer.py  # Document processing and AI analysis
│   ├── whatsapp_bot.py      # WhatsApp bot functionality
│   └── utils.py             # Utility functions
├── templates/               # HTML templates
│   ├── base.html
│   ├── index.html
│   └── result.html
├── static/                  # CSS, JS, and static assets
│   ├── css/style.css
│   └── js/main.js
└── requirements.txt         # Python dependencies
```

## Development

### Running in Development Mode
```bash
export FLASK_ENV=development
python app.py
```

### Testing Document Analysis
1. Create test documents in various formats (PDF, DOCX, TXT)
2. Upload through the web interface
3. Verify analysis results and formatting
4. Test error handling with invalid files

### WhatsApp Bot Testing
1. Configure Twilio webhook URL: `https://your-domain.com/webhook/whatsapp`
2. Send test messages to your WhatsApp number
3. Verify bot responses and functionality

## Deployment

### Production Deployment
```bash
# Install production server
pip install gunicorn

# Run with Gunicorn
gunicorn --bind 0.0.0.0:8000 app:app
```

### Docker Deployment
```dockerfile
FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
EXPOSE 5000
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "app:app"]
```

### Environment Variables for Production
- Set `FLASK_ENV=production`
- Use strong `FLASK_SECRET_KEY`
- Configure proper logging levels
- Set up HTTPS with SSL certificates

## Security Considerations

- Files are processed in memory and automatically cleaned up
- No permanent storage of uploaded documents
- Input validation and file type restrictions
- Secure API key management via environment variables
- CSRF protection enabled by default

## Limitations

- **Not Legal Advice**: This tool provides automated analysis for informational purposes only
- **AI Accuracy**: Analysis quality depends on OpenAI API and document quality
- **File Size**: Limited to documents under 10MB
- **Language**: Currently optimized for English legal documents

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support

For issues and questions:
1. Check the documentation above
2. Review existing GitHub issues
3. Create a new issue with detailed information

## Disclaimer

⚠️ **Important**: This tool is for informational purposes only and does not constitute legal advice. Always consult with qualified legal professionals for important legal matters.
