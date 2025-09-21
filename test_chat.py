#!/usr/bin/env python3
"""
Basic test script for JollyLLBot chat functionality
"""

import requests
import json
import sys
import time

def test_chat_api(base_url="http://127.0.0.1:5000"):
    """Test the chat API endpoints"""
    print("Testing JollyLLBot Chat API...")
    
    # Test messages and expected responses
    test_cases = [
        {
            'message': 'hello',
            'expected_contains': ['Welcome', 'JollyLLBot', 'Legal Document']
        },
        {
            'message': 'analyze',
            'expected_contains': ['Document Analysis', 'PDF', 'DOCX', 'TXT']
        },
        {
            'message': 'status',
            'expected_contains': ['Status', 'Active', 'Available', 'Ready']
        },
        {
            'message': 'unknown command',
            'expected_contains': ['understand', 'commands', 'help']
        }
    ]
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"\nTest {i}: Sending '{test_case['message']}'")
        
        try:
            # Send message to chat API
            response = requests.post(
                f"{base_url}/api/chat",
                json={'message': test_case['message']},
                headers={'Content-Type': 'application/json'},
                timeout=10
            )
            
            if response.status_code != 200:
                print(f"❌ HTTP Error: {response.status_code}")
                continue
            
            data = response.json()
            
            if 'error' in data:
                print(f"❌ API Error: {data['error']}")
                continue
            
            bot_response = data.get('response', '')
            print(f"✓ Bot responded: {bot_response[:100]}...")
            
            # Check if expected content is in response
            all_found = True
            for expected in test_case['expected_contains']:
                if expected.lower() not in bot_response.lower():
                    print(f"❌ Missing expected content: '{expected}'")
                    all_found = False
            
            if all_found:
                print("✓ All expected content found")
            
        except requests.exceptions.RequestException as e:
            print(f"❌ Request failed: {str(e)}")
        except json.JSONDecodeError as e:
            print(f"❌ JSON decode error: {str(e)}")
        except Exception as e:
            print(f"❌ Unexpected error: {str(e)}")

def test_chat_page(base_url="http://127.0.0.1:5000"):
    """Test that the chat page loads"""
    print("\nTesting chat page...")
    
    try:
        response = requests.get(f"{base_url}/chat", timeout=10)
        
        if response.status_code == 200:
            if 'JollyLLBot Chat' in response.text:
                print("✓ Chat page loads successfully")
                return True
            else:
                print("❌ Chat page content missing")
                return False
        else:
            print(f"❌ Chat page HTTP error: {response.status_code}")
            return False
            
    except requests.exceptions.RequestException as e:
        print(f"❌ Chat page request failed: {str(e)}")
        return False

def main():
    """Run all chat tests"""
    print("=" * 50)
    print("JollyLLBot Chat Interface Tests")
    print("=" * 50)
    
    base_url = "http://127.0.0.1:5000"
    
    # Test that the server is running
    try:
        requests.get(f"{base_url}/health", timeout=5)
        print(f"✓ Server is running at {base_url}")
    except requests.exceptions.RequestException:
        print(f"❌ Server not accessible at {base_url}")
        print("Please start the server with: python app.py")
        return 1
    
    # Run tests
    page_success = test_chat_page(base_url)
    if page_success:
        test_chat_api(base_url)
    
    print("\n" + "=" * 50)
    print("Chat tests completed!")
    print("=" * 50)
    
    return 0

if __name__ == "__main__":
    sys.exit(main())