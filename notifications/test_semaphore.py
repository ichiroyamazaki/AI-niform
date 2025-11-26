import requests
import json

# --- Semaphore setup ---
SEMAPHORE_API_KEY = "YOUR_SEMAPHORE_API_KEY_HERE"  # Replace with your Semaphore API key
SEMAPHORE_SENDER_NAME = "SCHOOL"  # Replace with your approved sender name
SEMAPHORE_URL = "https://api.semaphore.co/api/v4/messages"  # Semaphore API endpoint

def send_test_sms():
    """
    Send a test SMS using Semaphore API
    """
    # Test phone number (replace with your own number)
    test_number = "+639123456789"  # Replace with your test phone number
    test_message = "Test SMS from Semaphore - RFID Attendance System!"
    
    # Format phone number for Philippines
    if not test_number.startswith('+63'):
        if test_number.startswith('0'):
            test_number = '+63' + test_number[1:]
        elif test_number.startswith('63'):
            test_number = '+' + test_number
        else:
            test_number = '+63' + test_number
    
    # Prepare data for Semaphore API
    data = {
        'apikey': SEMAPHORE_API_KEY,
        'number': test_number,
        'message': test_message,
        'sendername': SEMAPHORE_SENDER_NAME
    }
    
    print("Sending test SMS via Semaphore...")
    print(f"To: {test_number}")
    print(f"Message: {test_message}")
    print(f"Sender: {SEMAPHORE_SENDER_NAME}")
    print("-" * 50)
    
    try:
        # Send SMS via Semaphore API
        response = requests.post(SEMAPHORE_URL, data=data)
        
        print(f"Response Status: {response.status_code}")
        print(f"Response Content: {response.text}")
        
        if response.status_code == 200:
            result = response.json()
            if result.get('status') == 'success':
                print("✅ SMS sent successfully!")
                print(f"Message ID: {result.get('message_id', 'N/A')}")
                print(f"Cost: {result.get('cost', 'N/A')}")
            else:
                print(f"❌ SMS failed: {result.get('message', 'Unknown error')}")
        else:
            print(f"❌ HTTP Error {response.status_code}")
            
    except Exception as e:
        print(f"❌ Error sending SMS: {str(e)}")

def check_balance():
    """
    Check Semaphore account balance
    """
    balance_url = "https://api.semaphore.co/api/v4/account"
    data = {'apikey': SEMAPHORE_API_KEY}
    
    try:
        response = requests.post(balance_url, data=data)
        if response.status_code == 200:
            result = response.json()
            print(f"Account Balance: ₱{result.get('balance', 'N/A')}")
            print(f"Credit Balance: ₱{result.get('credit_balance', 'N/A')}")
        else:
            print(f"❌ Error checking balance: {response.status_code}")
    except Exception as e:
        print(f"❌ Error checking balance: {str(e)}")

def check_sender_names():
    """
    Check available sender names
    """
    sender_url = "https://api.semaphore.co/api/v4/sender"
    data = {'apikey': SEMAPHORE_API_KEY}
    
    try:
        response = requests.post(sender_url, data=data)
        if response.status_code == 200:
            result = response.json()
            print("Available Sender Names:")
            for sender in result.get('data', []):
                print(f"- {sender.get('name', 'N/A')} (Status: {sender.get('status', 'N/A')})")
        else:
            print(f"❌ Error checking sender names: {response.status_code}")
    except Exception as e:
        print(f"❌ Error checking sender names: {str(e)}")

if __name__ == "__main__":
    print("Semaphore Test Script")
    print("=" * 50)
    print("Make sure to:")
    print("1. Replace YOUR_SEMAPHORE_API_KEY_HERE with your actual API key")
    print("2. Replace SCHOOL with your approved sender name")
    print("3. Replace +639123456789 with your test phone number")
    print("4. Add credits to your Semaphore account")
    print("=" * 50)
    print()
    
    # Check if API key is still placeholder
    if SEMAPHORE_API_KEY == "YOUR_SEMAPHORE_API_KEY_HERE":
        print("❌ Please update your Semaphore API key first!")
    else:
        print("Checking account information...")
        check_balance()
        print()
        check_sender_names()
        print()
        send_test_sms()



