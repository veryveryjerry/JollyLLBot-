// Chat Interface JavaScript

class ChatInterface {
    constructor() {
        this.messageInput = document.getElementById('messageInput');
        this.sendButton = document.getElementById('sendButton');
        this.chatMessages = document.getElementById('chatMessages');
        this.typingIndicator = document.getElementById('typingIndicator');
        
        this.init();
    }
    
    init() {
        // Event listeners
        this.sendButton.addEventListener('click', () => this.sendMessage());
        this.messageInput.addEventListener('keypress', (e) => {
            if (e.key === 'Enter') {
                this.sendMessage();
            }
        });
        
        // Focus on input
        this.messageInput.focus();
        
        // Auto-resize input
        this.messageInput.addEventListener('input', this.autoResizeInput.bind(this));
    }
    
    async sendMessage(text = null) {
        const message = text || this.messageInput.value.trim();
        if (!message) return;
        
        // Clear input if it's user input
        if (!text) {
            this.messageInput.value = '';
        }
        
        // Add user message to chat
        this.addMessage(message, 'user');
        
        // Show typing indicator
        this.showTypingIndicator();
        
        try {
            // Send message to bot
            const response = await this.sendToBot(message);
            
            // Hide typing indicator
            this.hideTypingIndicator();
            
            // Add bot response
            this.addMessage(response, 'bot');
            
        } catch (error) {
            console.error('Error sending message:', error);
            this.hideTypingIndicator();
            this.addMessage('Sorry, I encountered an error. Please try again later.', 'bot', true);
        }
        
        // Scroll to bottom
        this.scrollToBottom();
    }
    
    async sendToBot(message) {
        try {
            const response = await fetch('/api/chat', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ message: message })
            });
            
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            
            const data = await response.json();
            
            if (data.error) {
                throw new Error(data.error);
            }
            
            return data.response;
            
        } catch (error) {
            console.error('Error calling bot API:', error);
            // Fallback to mock response if API fails
            return this.generateBotResponse(message.toLowerCase());
        }
    }
    
    generateBotResponse(message) {
        // Simulate the WhatsApp bot's message processing logic
        if (message.includes('hello') || message.includes('hi') || message.includes('start') || message.includes('help')) {
            return `🏛️ Welcome to JollyLLBot - Legal Document Analysis Assistant!

I can help you analyze legal documents. Here's what I can do:

📄 Document Analysis
📋 Key Points Extraction  
⚠️ Risk Assessment
💡 Legal Recommendations

To get started:
1. Visit our web app to upload documents
2. Type 'analyze' for document analysis instructions
3. Type 'help' for more options

How can I assist you today?`;
        }
        
        if (message.includes('analyze') || message.includes('document')) {
            return `📄 Document Analysis Instructions:

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

Visit our web app or type 'help' for more options.`;
        }
        
        if (message.includes('status')) {
            return `🤖 JollyLLBot Status:

✅ WhatsApp Bot: Active
✅ Document Analysis: Available
✅ Web Interface: Online
⚙️ AI Engine: Ready

📊 Capabilities:
• PDF/DOCX/TXT Analysis
• Legal Risk Assessment
• Contract Review
• Document Summarization

Type 'help' for assistance or visit our web app!`;
        }
        
        // Default response
        return `🤔 I didn't quite understand that.

Try these commands:
• 'hello' - Get started
• 'analyze' - Document analysis info
• 'help' - Show available options  
• 'status' - Check system status

Or visit our web app for document upload and analysis!`;
    }
    
    addMessage(text, sender, isError = false) {
        const messageDiv = document.createElement('div');
        messageDiv.className = `message ${sender}-message${isError ? ' error-message' : ''}`;
        
        const avatar = document.createElement('div');
        avatar.className = 'message-avatar';
        avatar.innerHTML = sender === 'user' ? '<i class="fas fa-user"></i>' : '<i class="fas fa-robot"></i>';
        
        const content = document.createElement('div');
        content.className = 'message-content';
        
        const bubble = document.createElement('div');
        bubble.className = 'message-bubble';
        
        // Convert text to HTML, preserving line breaks and formatting
        const formattedText = this.formatMessage(text);
        bubble.innerHTML = formattedText;
        
        const time = document.createElement('div');
        time.className = 'message-time';
        time.textContent = this.getCurrentTime();
        
        content.appendChild(bubble);
        content.appendChild(time);
        
        messageDiv.appendChild(avatar);
        messageDiv.appendChild(content);
        
        this.chatMessages.appendChild(messageDiv);
        
        // Animate the message
        messageDiv.style.opacity = '0';
        messageDiv.style.transform = 'translateY(20px)';
        setTimeout(() => {
            messageDiv.style.transition = 'all 0.3s ease-out';
            messageDiv.style.opacity = '1';
            messageDiv.style.transform = 'translateY(0)';
        }, 10);
    }
    
    formatMessage(text) {
        // Convert line breaks to <br> tags
        let formatted = text.replace(/\n/g, '<br>');
        
        // Convert bullet points
        formatted = formatted.replace(/^• (.+)$/gm, '<li>$1</li>');
        
        // Wrap consecutive list items in <ul> tags
        formatted = formatted.replace(/(<li>.*<\/li>)(\s*<br>\s*<li>.*<\/li>)*/gm, '<ul>$&</ul>');
        formatted = formatted.replace(/<ul>(<li>.*<\/li>)(\s*<br>\s*<li>.*<\/li>)*<\/ul>/gm, (match) => {
            return '<ul>' + match.replace(/<ul>|<\/ul>/g, '').replace(/<br>\s*/g, '') + '</ul>';
        });
        
        // Convert numbered lists
        formatted = formatted.replace(/^(\d+)\. (.+)$/gm, '<div class="numbered-item"><strong>$1.</strong> $2</div>');
        
        // Make headings bold
        formatted = formatted.replace(/^([🏛️🤖📄📋⚠️💡🌐📱📊🤔]+.*):$/gm, '<p><strong>$1</strong></p>');
        
        return formatted;
    }
    
    getCurrentTime() {
        const now = new Date();
        return now.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
    }
    
    showTypingIndicator() {
        this.typingIndicator.style.display = 'block';
        this.scrollToBottom();
    }
    
    hideTypingIndicator() {
        this.typingIndicator.style.display = 'none';
    }
    
    scrollToBottom() {
        setTimeout(() => {
            this.chatMessages.scrollTop = this.chatMessages.scrollHeight;
        }, 100);
    }
    
    autoResizeInput() {
        this.messageInput.style.height = 'auto';
        this.messageInput.style.height = this.messageInput.scrollHeight + 'px';
    }
}

// Quick message functions
function sendQuickMessage(command) {
    if (window.chatInterface) {
        window.chatInterface.sendMessage(command);
    }
}

// Initialize chat interface when DOM is loaded
document.addEventListener('DOMContentLoaded', function() {
    window.chatInterface = new ChatInterface();
});

// Handle online/offline status
function updateOnlineStatus() {
    const statusIndicator = document.querySelector('.status-indicator');
    const statusText = statusIndicator.nextElementSibling;
    
    if (navigator.onLine) {
        statusIndicator.className = 'status-indicator online me-2';
        statusText.textContent = 'Online';
    } else {
        statusIndicator.className = 'status-indicator offline me-2';
        statusText.textContent = 'Offline';
    }
}

// Listen for online/offline events
window.addEventListener('online', updateOnlineStatus);
window.addEventListener('offline', updateOnlineStatus);

// Initialize status
document.addEventListener('DOMContentLoaded', updateOnlineStatus);