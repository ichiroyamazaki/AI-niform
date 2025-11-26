import requests
import json

# --- Txtbox setup ---
TXTBOX_API_KEY = "YOUR_TXTBOX_API_KEY_HERE"  # Replace with your Txtbox API key
TXTBOX_SENDER_NAME = "SCHOOL"  # Replace with your approved sender name
TXTBOX_URL = "https://api.txtbox.com/v1/sms/send"  # Txtbox API endpoint

def send_test_sms():
    """
    Send a test SMS using Txtbox API
    """
    # Test phone number (replace with your own number)
    test_number = "+639123456789"  # Replace with your test phone number
    test_message = "Test SMS from Txtbox - RFID Attendance System!"
    
    # Format phone number for Philippines
    if not test_number.startswith('+63'):
        if test_number.startswith('0'):
            test_number = '+63' + test_number[1:]
        elif test_number.startswith('63'):
            test_number = '+' + test_number
        else:
            test_number = '+63' + test_number
    
    # Prepare data for Txtbox API
    payload = {
        'api_key': TXTBOX_API_KEY,
        'sender_name': TXTBOX_SENDER_NAME,
        'recipient': test_number,
        'message': test_message
    }
    
    print("Sending test SMS via Txtbox...")
    print(f"To: {test_number}")
    print(f"Message: {test_message}")
    print(f"Sender: {TXTBOX_SENDER_NAME}")
    print("-" * 50)
    
    try:
        # Send SMS via Txtbox API
        response = requests.post(TXTBOX_URL, json=payload)
        
        print(f"Response Status: {response.status_code}")
        print(f"Response Content: {response.text}")
        
        if response.status_code == 200:
            result = response.json()
            if result.get('success') == True or result.get('status') == 'success':
                print("✅ SMS sent successfully!")
                print(f"Message ID: {result.get('message_id', result.get('id', 'N/A'))}")
                print(f"Cost: ₱{result.get('cost', '0.30')}")
            else:
                print(f"❌ SMS failed: {result.get('message', result.get('error', 'Unknown error'))}")
        else:
            print(f"❌ HTTP Error {response.status_code}")
            
    except Exception as e:
        print(f"❌ Error sending SMS: {str(e)}")

def check_balance():
    """
    Check Txtbox account balance
    """
    balance_url = "https://api.txtbox.com/v1/account/balance"
    payload = {'api_key': TXTBOX_API_KEY}
    
    try:
        response = requests.post(balance_url, json=payload)
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
    sender_url = "https://api.txtbox.com/v1/sender/names"
    payload = {'api_key': TXTBOX_API_KEY}
    
    try:
        response = requests.post(sender_url, json=payload)
        if response.status_code == 200:
            result = response.json()
            print("Available Sender Names:")
            for sender in result.get('data', []):
                print(f"- {sender.get('name', 'N/A')} (Status: {sender.get('status', 'N/A')})")
        else:
            print(f"❌ Error checking sender names: {response.status_code}")
    except Exception as e:
        print(f"❌ Error checking sender names: {str(e)}")

def check_pricing():
    """
    Display Txtbox pricing information
    """
    print("Txtbox Pricing Plans:")
    print("=" * 30)
    print("📱 Basic Plan: ₱0.30 per SMS")
    print("   - 1 Sender Name")
    print("   - ₱5,000 Purchase Limit")
    print("   - ₱50,000 Credit Limit")
    print()
    print("💼 Business Plan: ₱0.25 per SMS")
    print("   - 3 Sender Names")
    print("   - ₱100,000 Purchase Limit")
    print("   - ₱1,000,000 Credit Limit")
    print()
    print("🏢 Reseller Plan: <₱0.25 per SMS")
    print("   - Unlimited Sender Names")
    print("   - Unlimited Purchase/Credit Limits")
    print("=" * 30)

if __name__ == "__main__":
    print("Txtbox Test Script")
    print("=" * 50)
    print("Make sure to:")
    print("1. Replace YOUR_TXTBOX_API_KEY_HERE with your actual API key")
    print("2. Replace SCHOOL with your approved sender name")
    print("3. Replace +639123456789 with your test phone number")
    print("4. Add credits to your Txtbox account")
    print("5. Subscribe to a sender name (₱250/month)")
    print("=" * 50)
    print()
    
    # Check if API key is still placeholder
    if TXTBOX_API_KEY == "YOUR_TXTBOX_API_KEY_HERE":
        print("❌ Please update your Txtbox API key first!")
        print()
        check_pricing()
    else:
        print("Checking account information...")
        check_balance()
        print()
        check_sender_names()
        print()
        send_test_sms()



