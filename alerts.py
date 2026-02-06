import requests
import streamlit as st

# PASTE YOUR DISCORD WEBHOOK URL HERE
WEBHOOK_URL = "https://discord.com/api/webhooks/1469328578926874657/rCGr8TqdQLkf5RP-9GFZ5pbbTymR0xobvnKq8fZ3dy2ewZ8pJjp3B2Y-VxgAzIgXZnHK"

def send_discord_alert(device, ip, threat_score):
    """
    Sends a REAL notification to Discord. No passwords required.
    """
    try:
        # 1. Create the Message Payload (Hacker Style)
        payload = {
            "username": "Cyber-Rakshak Sentinel",
            "avatar_url": "https://cdn-icons-png.flaticon.com/512/9662/9662234.png",
            "embeds": [{
                "title": "🚨 RED ALERT: THREAT DETECTED",
                "description": f"**Anomaly Detected in IoT Network**",
                "color": 15548997, # Red Color
                "fields": [
                    {"name": "📍 Device", "value": device, "inline": True},
                    {"name": "🌐 Destination", "value": ip, "inline": True},
                    {"name": "🔥 Threat Score", "value": str(threat_score), "inline": False}
                ],
                "footer": {"text": "Action: Connection Severed | Admin Notified"}
            }]
        }
        
        # 2. Send it!
        response = requests.post(WEBHOOK_URL, json=payload)
        
        # 3. Check if it worked (Status 204 means success)
        if response.status_code == 204:
            return True
        else:
            return False
            
    except Exception as e:
        return False