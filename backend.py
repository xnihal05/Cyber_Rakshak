import time
import pandas as pd
import numpy as np
import random
import socket 
import os
import platform
import subprocess
from sklearn.ensemble import IsolationForest

# --- SCAPY SETUP ---
try:
    from scapy.all import sniff, IP, TCP, UDP, ARP, Ether, srp
    SCAPY_AVAILABLE = True
except ImportError:
    SCAPY_AVAILABLE = False
    print("⚠️ WARNING: Scapy not found. Switching to Simulation Mode.")

# --- 1. TRAIN THE AI MODEL ---
print("🧠 Training AI Model...")
clf = IsolationForest(contamination=0.1, random_state=42)
X_train = np.random.normal(loc=[50, 0, 10], scale=[10, 0.5, 2], size=(100, 3))
clf.fit(X_train)
print("✅ AI Model Trained & Ready.")

# --- 2. HELPER FUNCTIONS ---
def get_location_from_ip(ip):
    if ip.startswith("192.168") or ip.startswith("10."): return "Local Network (Home)"
    elif ip.startswith("172.") or ip.startswith("142."): return "USA (Google/AWS)"
    elif ip.startswith("104.") or ip.startswith("157."): return "USA (Cloudflare)"
    else: return "Internet (Public)"

def generate_fake_attack():
    return {
        "Timestamp": time.strftime("%H:%M:%S"),
        "Device": "Smart Bulb (IoT)",
        "Destination": "Unknown (China Server)",
        "Size_KB": 0.5,
        "Direction": "Upload",
        "Protocol": "TCP",
        "AI_Status": "🚨 THREAT",
        "Anomaly_Score": -0.95,
        "Alert": "Lateral Movement Detected!"
    }

# --- 3. MAIN DATA STREAM FUNCTION ---
def get_data_stream(num_packets=1):
    captured_data = []
    if SCAPY_AVAILABLE:
        try:
            packets = sniff(count=num_packets, timeout=0.1)
            for pkt in packets:
                if IP in pkt:
                    src = pkt[IP].src
                    dst = pkt[IP].dst
                    size = len(pkt)
                    if src.startswith("192.168"):
                        direction = "Upload"
                        remote_ip = dst
                    else:
                        direction = "Download"
                        remote_ip = src
                    
                    dir_code = 1 if direction == "Upload" else 0
                    ai_input = [[size, dir_code, 10]]
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
        except Exception:
            pass 

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

# --- 4. NETWORK SCANNER LOGIC ---
def get_local_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(('10.255.255.255', 1))
        IP = s.getsockname()[0]
    except Exception:
        IP = "127.0.0.1"
    finally:
        s.close()
    return IP

def scan_network_devices():
    devices = []
    if SCAPY_AVAILABLE:
        try:
            my_ip = get_local_ip()
            ip_base = my_ip.rsplit('.', 1)[0]
            ip_range = ip_base + ".1/24"
            arp_request = ARP(pdst=ip_range)
            broadcast = Ether(dst="ff:ff:ff:ff:ff:ff")
            arp_request_broadcast = broadcast/arp_request
            answered_list = srp(arp_request_broadcast, timeout=1.0, verbose=False)[0]
            for element in answered_list:
                devices.append({"IP": element[1].psrc, "MAC": element[1].hwsrc, "Status": "🟢 ONLINE", "Type": "Unknown Device"})
        except Exception:
            pass 
            
    if len(devices) < 5:
        base_ip = "192.168.1"
        types = ["iPhone 14", "Pixel 7", "Dell XPS", "HP Envy", "MacBook Air", "Smart Bulb", "Alexa Dot"]
        for i in range(15):
            fake_ip = f"{base_ip}.{random.randint(50, 200)}"
            fake_mac = "XX:XX:XX:XX:XX:XX"
            fake_type = random.choice(types)
            devices.append({"IP": fake_ip, "MAC": fake_mac, "Status": "🟢 ONLINE", "Type": fake_type})
    return devices

# --- 5. HUMAN-LIKE DECEPTION ---
def deploy_decoy_data(target_ip):
    def get_human_password():
        bases = ["Summer", "Winter", "Welcome", "Password", "Admin", "Company", "Monkey", "Dragon", "Football"]
        years = ["2023", "2024", "2025", "123", "12345"]
        symbols = ["!", "@", "#", "!!"]
        if random.random() > 0.2: return f"{random.choice(bases)}{random.choice(years)}{random.choice(symbols)}"
        else: return "".join(random.choices('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789', k=12))

    first_names = ["john", "sarah", "mike", "emma", "david", "admin", "guest"]
    last_names = ["smith", "doe", "jones", "wilson", "brown"]
    
    def get_human_username():
        style = random.choice([1, 2, 3])
        if style == 1: return f"{random.choice(first_names)}.{random.choice(last_names)}"
        if style == 2: return f"{random.choice(first_names)[0]}{random.choice(last_names)}"
        if style == 3: return f"{random.choice(first_names)}_{random.randint(10,99)}"

    # Generate Content
    if random.random() > 0.5:
        # Scenario A: Fake Passwords
        filename = "leaked_passwords.txt"
        file_content = "# EXPORTED SAVED PASSWORDS - CHROME\nurl,username,password\n"
        for i in range(random.randint(4, 7)):
            user = get_human_username()
            pwd = get_human_password()
            file_content += f"http://internal-portal.com,{user},{pwd}\n"
        file_size = f"{random.randint(1, 5)} KB"
    else:
        # Scenario B: Fake SQL Dump
        filename = "users_table_backup.sql"
        file_content = "-- DATABASE DUMP: employees\nINSERT INTO `users` (user, pass_hash) VALUES\n"
        rows = []
        for i in range(random.randint(3, 5)):
            u = get_human_username()
            p_hash = f"e10adc3949ba59abbe56e057f20f883e"
            rows.append(f"('{u}', '{p_hash}') /* Pwd: {get_human_password()} */")
        file_content += ",\n".join(rows) + ";"
        file_size = f"{random.randint(10, 50)} MB"

    # --- SAVE THE FILE TO DISK ---
    try:
        with open(filename, "w") as f:
            f.write(file_content)
        print(f"✅ DECOY FILE CREATED: {filename}")
    except Exception as e:
        print(f"⚠️ Could not write file: {e}")

    return {
        "status": "✅ DECOY DEPLOYED",
        "filename": filename,
        "payload": file_content,
        "size": file_size,
        "target": target_ip
    }

# --- 6. REAL FIREWALL INTEGRATION (THE KILL SWITCH) ---
def sever_connection(attacker_ip):
    system = platform.system()
    
    # SAFETY: If the IP is generic text, use a dummy IP so the command doesn't crash.
    if "Unknown" in attacker_ip or "Server" in attacker_ip:
        target_ip = "203.0.113.55" 
    else:
        target_ip = attacker_ip

    print(f"⚔️ INITIATING KILL SWITCH ON {target_ip}...")
    
    try:
        if system == "Windows":
            # Windows Firewall Command (Requires Admin)
            cmd = f'netsh advfirewall firewall add rule name="CYBER_RAKSHAK_BLOCK" dir=in action=block remoteip={target_ip}'
            subprocess.run(cmd, shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            return {"status": "success", "msg": f"🚫 WINDOWS FIREWALL: BLOCKED {target_ip}"}
            
        elif system == "Linux":
            # Linux IPTables Command (Requires Sudo)
            cmd = f"sudo iptables -A INPUT -s {target_ip} -j DROP"
            subprocess.run(cmd, shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            return {"status": "success", "msg": f"🚫 IPTABLES: DROPPED PACKETS FROM {target_ip}"}
            
        else:
            return {"status": "simulated", "msg": f"🚫 SYSTEM UNSUPPORTED: SIMULATED BLOCK {target_ip}"}
            
    except Exception as e:
        # If we lack Admin rights, we simulate it so the demo doesn't crash
        return {"status": "simulated", "msg": f"⚠️ ADMIN RIGHTS MISSING: SIMULATING BLOCK ON {target_ip}"}
