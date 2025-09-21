"""
WhatsApp Bot Module
Handles WhatsApp integration using Twilio
"""

import os
import logging
from flask import request
from twilio.rest import Client
from twilio.twiml.messaging_response import MessagingResponse

logger = logging.getLogger(__name__)


class WhatsAppBot:
    """WhatsApp bot for legal document analysis"""
    
    def __init__(self):
        """Initialize Twilio client"""
        account_sid = os.getenv('TWILIO_ACCOUNT_SID')
        auth_token = os.getenv('TWILIO_AUTH_TOKEN')
        self.whatsapp_number = os.getenv('TWILIO_WHATSAPP_NUMBER', 'whatsapp:+14155238886')
        
        if account_sid and auth_token:
            self.client = Client(account_sid, auth_token)
            logger.info("Twilio client initialized successfully")
        else:
            self.client = None
            logger.warning("Twilio credentials not found. WhatsApp bot will use mock responses.")
    
    def handle_message(self, request):
        """Handle incoming WhatsApp message"""
        try:
            # Get message details
            from_number = request.values.get('From', '')
            message_body = request.values.get('Body', '').strip().lower()
            
            logger.info(f"Received WhatsApp message from {from_number}: {message_body}")
            
            # Create response
            response = MessagingResponse()
            msg = response.message()
            
            # Process message based on content
            if message_body in ['hello', 'hi', 'start', 'help']:
                reply_text = self._get_welcome_message()
            elif 'analyze' in message_body or 'document' in message_body:
                reply_text = self._get_document_instructions()
            elif 'status' in message_body:
                reply_text = self._get_status_message()
            else:
                reply_text = self._get_default_message()
            
            msg.body(reply_text)
            
            return str(response)
            
        except Exception as e:
            logger.error(f"Error handling WhatsApp message: {str(e)}")
            response = MessagingResponse()
            msg = response.message()
            msg.body("Sorry, I encountered an error. Please try again later.")
            return str(response)
    
    def send_message(self, to_number: str, message: str):
        """Send a message to a WhatsApp number"""
        if not self.client:
            logger.warning("Cannot send message - Twilio client not initialized")
            return False
        
        try:
            message = self.client.messages.create(
                body=message,
                from_=self.whatsapp_number,
                to=to_number
            )
            logger.info(f"Message sent to {to_number}: {message.sid}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to send message: {str(e)}")
            return False
    
    def _get_welcome_message(self) -> str:
        """Get welcome message for new users"""
        return """🏛️ Welcome to JollyLLBot - Legal Document Analysis Assistant!

I can help you analyze legal documents. Here's what I can do:

📄 Document Analysis
📋 Key Points Extraction  
⚠️ Risk Assessment
💡 Legal Recommendations

To get started:
1. Visit our web app to upload documents
2. Type 'analyze' for document analysis instructions
3. Type 'help' for more options

How can I assist you today?"""
    
    def _get_document_instructions(self) -> str:
        """Get document analysis instructions"""
        return """📄 Document Analysis Instructions:

Currently, document upload is available through our web interface. 

🌐 Web App Features:
• Upload PDF, DOCX, or TXT files
• Get instant AI-powered analysis
• Receive detailed legal insights
• Download analysis reports

📱 Coming Soon:
• Direct document upload via WhatsApp
• Voice message analysis
• Quick legal Q&A

Visit our web app or type 'help' for more options."""
    
    def _get_status_message(self) -> str:
        """Get system status message"""
        return """🤖 JollyLLBot Status:

✅ WhatsApp Bot: Active
✅ Document Analysis: Available
✅ Web Interface: Online
⚙️ AI Engine: Ready

📊 Capabilities:
• PDF/DOCX/TXT Analysis
• Legal Risk Assessment
• Contract Review
• Document Summarization

Type 'help' for assistance or visit our web app!"""
    
    def _get_default_message(self) -> str:
        """Get default response for unrecognized messages"""
        return """🤔 I didn't quite understand that.

Try these commands:
• 'hello' - Get started
• 'analyze' - Document analysis info
• 'help' - Show available options  
• 'status' - Check system status

Or visit our web app for document upload and analysis!"""
    
    def notify_analysis_complete(self, phone_number: str, filename: str, summary: str):
        """Notify user when document analysis is complete"""
        message = f"""✅ Document Analysis Complete!

📄 File: {filename}
📋 Summary: {summary[:200]}...

View full analysis on our web app or request more details."""
        
        return self.send_message(phone_number, message)