import requests
import json

# --- CloudSMS setup ---
CLOUDSMS_API_KEY = "YOUR_CLOUDSMS_API_KEY_HERE"  # Replace with your CloudSMS API key
CLOUDSMS_SENDER_NAME = "SCHOOL"  # Replace with your approved sender name
CLOUDSMS_URL = "https://api.cloudsms.com.ph/api/send"  # CloudSMS API endpoint

def send_test_sms():
    """
    Send a test SMS using CloudSMS API
    """
    # Test phone number (replace with your own number)
    test_number = "+639123456789"  # Replace with your test phone number
    test_message = "Test SMS from CloudSMS - RFID Attendance System!"
    
    # Format phone number for Philippines
    if not test_number.startswith('+63'):
        if test_number.startswith('0'):
            test_number = '+63' + test_number[1:]
        elif test_number.startswith('63'):
            test_number = '+' + test_number
        else:
            test_number = '+63' + test_number
    
    # Prepare data for CloudSMS API
    data = {
        'api_key': CLOUDSMS_API_KEY,
        'to': test_number,
        'message': test_message,
        'from': CLOUDSMS_SENDER_NAME
    }
    
    print("Sending test SMS via CloudSMS...")
    print(f"To: {test_number}")
    print(f"Message: {test_message}")
    print(f"Sender: {CLOUDSMS_SENDER_NAME}")
    print("-" * 50)
    
    try:
        # Send SMS via CloudSMS API
        response = requests.post(CLOUDSMS_URL, data=data)
        
        print(f"Response Status: {response.status_code}")
        print(f"Response Content: {response.text}")
        
        if response.status_code == 200:
            result = response.json()
            if result.get('success') == True or result.get('status') == 'success':
                print("✅ SMS sent successfully!")
                print(f"Message ID: {result.get('message_id', result.get('id', 'N/A'))}")
                print(f"Cost: {result.get('cost', 'N/A')}")
            else:
                print(f"❌ SMS failed: {result.get('message', result.get('error', 'Unknown error'))}")
        else:
            print(f"❌ HTTP Error {response.status_code}")
            
    except Exception as e:
        print(f"❌ Error sending SMS: {str(e)}")

def check_balance():
    """
    Check CloudSMS account balance
    """
    balance_url = "https://api.cloudsms.com.ph/api/balance"
    data = {'api_key': CLOUDSMS_API_KEY}
    
    try:
        response = requests.post(balance_url, data=data)
        if response.status_code == 200:
            result = response.json()
            print(f"Account Balance: ₱{result.get('balance', 'N/A')}")
        else:
            print(f"❌ Error checking balance: {response.status_code}")
    except Exception as e:
        print(f"❌ Error checking balance: {str(e)}")

if __name__ == "__main__":
    print("CloudSMS Test Script")
    print("=" * 50)
    print("Make sure to:")
    print("1. Replace YOUR_CLOUDSMS_API_KEY_HERE with your actual API key")
    print("2. Replace SCHOOL with your approved sender name")
    print("3. Replace +639123456789 with your test phone number")
    print("4. Add credits to your CloudSMS account")
    print("=" * 50)
    print()
    
    # Check if API key is still placeholder
    if CLOUDSMS_API_KEY == "YOUR_CLOUDSMS_API_KEY_HERE":
        print("❌ Please update your CloudSMS API key first!")
    else:
        print("Checking account balance...")
        check_balance()
        print()
        send_test_sms()



