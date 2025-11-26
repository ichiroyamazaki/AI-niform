import requests
import json

# --- PhilSMS setup ---
PHILSMS_API_KEY = "YOUR_PHILSMS_API_KEY_HERE"  # Replace with your PhilSMS API key
PHILSMS_SENDER_NAME = "SCHOOL"  # Replace with your approved sender name
PHILSMS_URL = "https://api.philsms.com/v1/send"  # PhilSMS API endpoint

def send_test_sms():
    """
    Send a test SMS using PhilSMS API
    """
    # Test phone number (replace with your own number)
    test_number = "+639123456789"  # Replace with your verified phone number
    test_message = "Test SMS from PhilSMS - RFID Attendance System!"
    
    # Format phone number for Philippines
    if not test_number.startswith('+63'):
        if test_number.startswith('0'):
            test_number = '+63' + test_number[1:]
        elif test_number.startswith('63'):
            test_number = '+' + test_number
        else:
            test_number = '+63' + test_number
    
    # Prepare data for PhilSMS API
    data = {
        'apikey': PHILSMS_API_KEY,
        'number': test_number,
        'message': test_message,
        'sendername': PHILSMS_SENDER_NAME
    }
    
    print("Sending test SMS via PhilSMS...")
    print(f"To: {test_number}")
    print(f"Message: {test_message}")
    print(f"Sender: {PHILSMS_SENDER_NAME}")
    print("-" * 50)
    
    try:
        # Send SMS via PhilSMS API
        response = requests.post(PHILSMS_URL, data=data)
        
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

if __name__ == "__main__":
    print("PhilSMS Test Script")
    print("=" * 50)
    print("Make sure to:")
    print("1. Replace YOUR_PHILSMS_API_KEY_HERE with your actual API key")
    print("2. Replace SCHOOL with your approved sender name")
    print("3. Replace +639123456789 with your test phone number")
    print("4. Add credits to your PhilSMS account")
    print("=" * 50)
    print()
    
    # Check if API key is still placeholder
    if PHILSMS_API_KEY == "YOUR_PHILSMS_API_KEY_HERE":
        print("❌ Please update your PhilSMS API key first!")
    else:
        send_test_sms()



