"""
Utility functions for the JollyLLBot application
"""

import os
import logging
from typing import Set


def allowed_file(filename: str) -> bool:
    """Check if file extension is allowed"""
    allowed_extensions = set(os.getenv('ALLOWED_EXTENSIONS', 'pdf,docx,txt').split(','))
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in allowed_extensions


def get_allowed_extensions() -> Set[str]:
    """Get set of allowed file extensions"""
    return set(os.getenv('ALLOWED_EXTENSIONS', 'pdf,docx,txt').split(','))


def setup_logging(log_level: str = 'INFO'):
    """Setup logging configuration"""
    logging.basicConfig(
        level=getattr(logging, log_level),
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.StreamHandler(),
            logging.FileHandler('jollybot.log') if os.path.exists('.') else logging.NullHandler()
        ]
    )


def validate_file_size(file_path: str, max_size_mb: int = 10) -> bool:
    """Validate file size"""
    try:
        file_size = os.path.getsize(file_path)
        max_size_bytes = max_size_mb * 1024 * 1024
        return file_size <= max_size_bytes
    except OSError:
        return False


def sanitize_filename(filename: str) -> str:
    """Sanitize filename for safe storage"""
    import re
    # Remove any non-alphanumeric characters except dots and dashes
    sanitized = re.sub(r'[^a-zA-Z0-9.-]', '_', filename)
    return sanitized[:100]  # Limit length


def format_file_size(size_bytes: int) -> str:
    """Format file size in human readable format"""
    if size_bytes < 1024:
        return f"{size_bytes} B"
    elif size_bytes < 1024**2:
        return f"{size_bytes/1024:.1f} KB"
    elif size_bytes < 1024**3:
        return f"{size_bytes/(1024**2):.1f} MB"
    else:
        return f"{size_bytes/(1024**3):.1f} GB"


def truncate_text(text: str, max_length: int = 100) -> str:
    """Truncate text to specified length"""
    if len(text) <= max_length:
        return text
    return text[:max_length-3] + "..."