import time
import pandas as pd
import numpy as np
import random
from sklearn.ensemble import IsolationForest


try:
    from scapy.all import sniff, IP, TCP, UDP
    SCAPY_AVAILABLE = True
except ImportError:
    SCAPY_AVAILABLE = False
    print("⚠️ WARNING: Scapy not found. Switching to Simulation Mode.")

# --- 1. TRAIN THE AI MODEL (Isolation Forest) ---
# We train it instantly when the app starts.
print("🧠 Training AI Model...")
clf = IsolationForest(contamination=0.1, random_state=42)

# Create dummy 'normal' data to teach the AI what safe traffic looks like
# Features: [Packet Size, Direction (0=Down, 1=Up), Frequency]
X_train = np.random.normal(loc=[50, 0, 10], scale=[10, 0.5, 2], size=(100, 3))
clf.fit(X_train)
print("✅ AI Model Trained & Ready.")

# --- 2. HELPER FUNCTIONS ---
def get_location_from_ip(ip):
    # Makes IPs look realistic for the demo
    if ip.startswith("192.168") or ip.startswith("10."):
        return "Local Network (Home)"
    elif ip.startswith("172.") or ip.startswith("142."): 
        return "USA (Google/AWS)"
    elif ip.startswith("104.") or ip.startswith("157."):
        return "USA (Cloudflare)"
    else:
        return "Internet (Public)"

def generate_fake_attack():
    """
    Creates a FAKE packet that looks exactly like a Chinese Spy Chip.
    We use this when you press the 'Simulate Attack' button.
    """
    return {
        "Timestamp": time.strftime("%H:%M:%S"),
        "Device": "Smart Bulb (IoT)",
        "Destination": "Unknown (China Server)",
        "Size_KB": 0.5,     # Tiny 'heartbeat' packet
        "Direction": "Upload",
        "Protocol": "TCP",
        "AI_Status": "🚨 THREAT",
        "Anomaly_Score": -0.95, # High Threat Score
        "Alert": "Lateral Movement Detected!"
    }

# --- 3. MAIN DATA STREAM FUNCTION ---
def get_data_stream(num_packets=1):
    """
    Tries to get REAL data. If Scapy fails or finds nothing, returns a 'Waiting' signal.
    """
    captured_data = []
    
    if SCAPY_AVAILABLE:
        # Listen to the Wi-Fi card for 0.5 seconds
        packets = sniff(count=num_packets, timeout=0.1)
        
        for pkt in packets:
            if IP in pkt:
                src = pkt[IP].src
                dst = pkt[IP].dst
                size = len(pkt)
                
                # Guess direction based on IP
                if src.startswith("192.168"):
                    direction = "Upload"
                    remote_ip = dst
                else:
                    direction = "Download"
                    remote_ip = src
                
                # Prepare data for AI
                dir_code = 1 if direction == "Upload" else 0
                ai_input = [[size, dir_code, 10]]
                
                # Ask AI: Is this safe?
                pred = clf.predict(ai_input)[0]
                status = "✅ SAFE" if pred == 1 else "⚠️ CHECK"
                
                captured_data.append({
                    "Timestamp": time.strftime("%H:%M:%S"),
                    "Device": "My Laptop",
                    "Destination": get_location_from_ip(remote_ip),
                    "Size_KB": size,
                    "Direction": direction,
                    "Protocol": "TCP" if TCP in pkt else "UDP",
                    "AI_Status": status,
                    "Anomaly_Score": 0.15,
                    "Alert": "-"
                })

    # If we didn't catch any real packets, return an Idle packet
    if not captured_data:
        return [{
            "Timestamp": time.strftime("%H:%M:%S"),
            "Device": "Network Idle",
            "Destination": "-",
            "Size_KB": 0,
            "Direction": "-",
            "Protocol": "-",
            "AI_Status": "💤 IDLE",
            "Anomaly_Score": 0.0,
            "Alert": "-"
        }]
        
    return captured_data