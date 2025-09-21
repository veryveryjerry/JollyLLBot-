#!/usr/bin/env python3
"""
Basic test script for JollyLLBot functionality
"""

import os
import sys
import tempfile
from src.document_analyzer import DocumentAnalyzer
from src.whatsapp_bot import WhatsAppBot
from src.utils import allowed_file, setup_logging

def test_document_analyzer():
    """Test document analyzer functionality"""
    print("Testing DocumentAnalyzer...")
    
    analyzer = DocumentAnalyzer()
    
    # Test with a simple text file
    with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as f:
        f.write("This is a test contract agreement between parties A and B.")
        test_file = f.name
    
    try:
        # Test text extraction
        text = analyzer.extract_text(test_file)
        assert len(text) > 0, "Text extraction failed"
        print(f"✓ Text extraction: {len(text)} characters")
        
        # Test document analysis
        result = analyzer.analyze_document(test_file)
        assert result['success'] == True, "Document analysis failed"
        assert 'analysis' in result, "Analysis missing from result"
        print(f"✓ Document analysis: {result['word_count']} words")
        print(f"✓ Document type: {result['analysis']['document_type']}")
        
    finally:
        os.unlink(test_file)
    
    print("DocumentAnalyzer tests passed!\n")

def test_whatsapp_bot():
    """Test WhatsApp bot functionality"""
    print("Testing WhatsAppBot...")
    
    bot = WhatsAppBot()
    
    # Test message responses
    welcome = bot._get_welcome_message()
    assert "JollyLLBot" in welcome, "Welcome message missing bot name"
    print("✓ Welcome message generated")
    
    instructions = bot._get_document_instructions()
    assert "document" in instructions.lower(), "Instructions missing document info"
    print("✓ Document instructions generated")
    
    status = bot._get_status_message()
    assert "Status" in status, "Status message missing status info"
    print("✓ Status message generated")
    
    print("WhatsAppBot tests passed!\n")

def test_utils():
    """Test utility functions"""
    print("Testing utility functions...")
    
    # Test file validation
    assert allowed_file("test.pdf") == True, "PDF files should be allowed"
    assert allowed_file("test.docx") == True, "DOCX files should be allowed"
    assert allowed_file("test.txt") == True, "TXT files should be allowed"
    assert allowed_file("test.exe") == False, "EXE files should not be allowed"
    print("✓ File validation working")
    
    # Test logging setup
    setup_logging()
    print("✓ Logging setup successful")
    
    print("Utility function tests passed!\n")

def main():
    """Run all tests"""
    print("=" * 50)
    print("JollyLLBot Basic Functionality Tests")
    print("=" * 50)
    
    try:
        test_utils()
        test_document_analyzer()
        test_whatsapp_bot()
        
        print("=" * 50)
        print("All tests passed! ✅")
        print("JollyLLBot is ready for use.")
        print("=" * 50)
        return 0
        
    except Exception as e:
        print(f"❌ Test failed: {str(e)}")
        import traceback
        traceback.print_exc()
        return 1

if __name__ == "__main__":
    sys.exit(main())