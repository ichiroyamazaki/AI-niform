import firebase_admin
from firebase_admin import credentials, db
import requests
import json

# --- Txtbox setup ---
TXTBOX_API_KEY = "YOUR_TXTBOX_API_KEY_HERE"  # Replace with your Txtbox API key
TXTBOX_SENDER_NAME = "SCHOOL"  # Replace with your approved sender name
TXTBOX_URL = "https://api.txtbox.com/v1/sms/send"  # Txtbox API endpoint

# --- Firebase setup ---
cred = credentials.Certificate("serviceAccountKey.json")  # JSON file in your project folder
firebase_admin.initialize_app(cred, {
    "databaseURL": "https://school-attendance-63ead-default-rtdb.asia-southeast1.firebasedatabase.app/"
})

def send_sms(to, message):
    """
    Send SMS using Txtbox API
    """
    # Format phone number for Philippines (add +63 if needed)
    if not to.startswith('+63'):
        if to.startswith('0'):
            to = '+63' + to[1:]  # Remove leading 0 and add +63
        elif to.startswith('63'):
            to = '+' + to  # Add + if missing
        else:
            to = '+63' + to  # Add +63 prefix
    
    # Prepare data for Txtbox API
    payload = {
        'api_key': TXTBOX_API_KEY,
        'sender_name': TXTBOX_SENDER_NAME,
        'recipient': to,
        'message': message
    }
    
    try:
        # Send SMS via Txtbox API
        response = requests.post(TXTBOX_URL, json=payload)
        
        if response.status_code == 200:
            result = response.json()
            if result.get('success') == True or result.get('status') == 'success':
                print(f"✅ SMS sent to {to}: {message}")
                print(f"Message ID: {result.get('message_id', result.get('id', 'N/A'))}")
                print(f"Cost: ₱{result.get('cost', '0.30')}")
            else:
                print(f"❌ SMS failed: {result.get('message', result.get('error', 'Unknown error'))}")
        else:
            print(f"❌ HTTP Error {response.status_code}: {response.text}")
            
    except Exception as e:
        print(f"❌ Error sending SMS: {str(e)}")

# --- Main loop ---
print("Place your RFID card on the reader...")

while True:
    uid = input("Scan card: ").strip()  # USB RFID reader types UID like a keyboard

    student = db.reference("/students/" + uid).get()
    if student:
        message = f"{student['name']} ({student['grade']}) has entered the school."
        send_sms(student["parent_contact"], message)
    else:
        print("No student found for UID:", uid)
