// JollyLLBot Main JavaScript

document.addEventListener('DOMContentLoaded', function() {
    // Initialize tooltips
    var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });

    // File upload validation
    const fileInput = document.getElementById('file');
    if (fileInput) {
        fileInput.addEventListener('change', function(e) {
            validateFile(e.target.files[0]);
        });
    }

    // Form submission handling
    const uploadForm = document.getElementById('uploadForm');
    if (uploadForm) {
        uploadForm.addEventListener('submit', function(e) {
            const file = fileInput.files[0];
            if (!file) {
                e.preventDefault();
                showAlert('Please select a file to upload.', 'warning');
                return;
            }
            
            if (!validateFile(file)) {
                e.preventDefault();
                return;
            }
            
            showLoadingState();
        });
    }
});

function validateFile(file) {
    if (!file) return false;
    
    const maxSize = 10 * 1024 * 1024; // 10MB
    const allowedTypes = ['application/pdf', 'application/vnd.openxmlformats-officedocument.wordprocessingml.document', 'text/plain'];
    const allowedExtensions = ['.pdf', '.docx', '.txt'];
    
    // Check file size
    if (file.size > maxSize) {
        showAlert('File size must be less than 10MB.', 'danger');
        return false;
    }
    
    // Check file type
    const fileName = file.name.toLowerCase();
    const isValidExtension = allowedExtensions.some(ext => fileName.endsWith(ext));
    const isValidType = allowedTypes.includes(file.type);
    
    if (!isValidExtension && !isValidType) {
        showAlert('Please upload a PDF, DOCX, or TXT file.', 'danger');
        return false;
    }
    
    return true;
}

function showLoadingState() {
    const btn = document.getElementById('analyzeBtn');
    const modal = document.getElementById('loadingModal');
    
    if (btn) {
        btn.disabled = true;
        btn.innerHTML = '<i class="fas fa-spinner fa-spin me-2"></i>Analyzing...';
    }
    
    if (modal) {
        const bootstrapModal = new bootstrap.Modal(modal);
        bootstrapModal.show();
    }
}

function showAlert(message, type = 'info') {
    const alertHtml = `
        <div class="alert alert-${type} alert-dismissible fade show" role="alert">
            ${message}
            <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
        </div>
    `;
    
    // Insert alert at the top of the main content
    const main = document.querySelector('main');
    if (main) {
        main.insertAdjacentHTML('afterbegin', alertHtml);
    }
}

// API helper functions
async function analyzeDocumentAPI(file) {
    const formData = new FormData();
    formData.append('file', file);
    
    try {
        const response = await fetch('/api/analyze', {
            method: 'POST',
            body: formData
        });
        
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        
        return await response.json();
    } catch (error) {
        console.error('Analysis API error:', error);
        throw error;
    }
}

// Utility functions
function formatFileSize(bytes) {
    if (bytes === 0) return '0 Bytes';
    
    const k = 1024;
    const sizes = ['Bytes', 'KB', 'MB', 'GB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    
    return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
}

function copyToClipboard(text) {
    navigator.clipboard.writeText(text).then(function() {
        showAlert('Copied to clipboard!', 'success');
    }).catch(function(err) {
        console.error('Could not copy text: ', err);
        showAlert('Failed to copy to clipboard.', 'danger');
    });
}

// Download functionality
function downloadResults(data, filename = 'analysis_results.json') {
    const blob = new Blob([JSON.stringify(data, null, 2)], {
        type: 'application/json'
    });
    
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = filename;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
}

// Health check functionality
async function checkSystemHealth() {
    try {
        const response = await fetch('/health');
        const data = await response.json();
        
        if (data.status === 'healthy') {
            updateHealthStatus('online', 'System is healthy');
        } else {
            updateHealthStatus('warning', 'System status unknown');
        }
    } catch (error) {
        updateHealthStatus('offline', 'System is offline');
    }
}

function updateHealthStatus(status, message) {
    const indicator = document.querySelector('.status-indicator');
    if (indicator) {
        indicator.className = `status-indicator status-${status}`;
        indicator.title = message;
    }
}

// Auto-refresh health status every 30 seconds
setInterval(checkSystemHealth, 30000);

// Progressive Web App functionality
if ('serviceWorker' in navigator) {
    window.addEventListener('load', function() {
        navigator.serviceWorker.register('/static/js/sw.js')
            .then(function(registration) {
                console.log('ServiceWorker registration successful');
            })
            .catch(function(err) {
                console.log('ServiceWorker registration failed');
            });
    });
}

// Keyboard shortcuts
document.addEventListener('keydown', function(e) {
    // Ctrl/Cmd + U to focus upload input
    if ((e.ctrlKey || e.metaKey) && e.key === 'u') {
        e.preventDefault();
        const fileInput = document.getElementById('file');
        if (fileInput) {
            fileInput.click();
        }
    }
    
    // Escape to close modals
    if (e.key === 'Escape') {
        const modals = document.querySelectorAll('.modal.show');
        modals.forEach(modal => {
            const bootstrapModal = bootstrap.Modal.getInstance(modal);
            if (bootstrapModal) {
                bootstrapModal.hide();
            }
        });
    }
});