from twilio.rest import Client

# --- Twilio setup ---
# IMPORTANT: Replace these with your own Twilio credentials
# Get your credentials from: https://console.twilio.com/
account_sid = "YOUR_TWILIO_ACCOUNT_SID_HERE"
auth_token = "YOUR_TWILIO_AUTH_TOKEN_HERE"
twilio_number = "YOUR_TWILIO_PHONE_NUMBER"     # Your Twilio trial number
to_number = "YOUR_VERIFIED_PHONE_NUMBER"        # Your verified PH number

client = Client(account_sid, auth_token)

print("📡 Sending test SMS...")

try:
    message = client.messages.create(
        body="🚀 Test SMS from Twilio trial account to your PH number!",
        from_=twilio_number,
        to=to_number
    )
    print("✅ Message sent successfully!")
    print("Message SID:", message.sid)
except Exception as e:
    print("❌ Error while sending SMS:")
    print(str(e))
