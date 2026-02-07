# 🛡️ Cyber-Rakshak: Autonomous IoT Defense System
> *Defender of the Connected World.*

![Project Banner](https://img.shields.io/badge/Status-Prototype%20v2.0-success?style=for-the-badge)
![Python](https://img.shields.io/badge/Python-3.10-blue?style=for-the-badge&logo=python&logoColor=white)
![Streamlit](https://img.shields.io/badge/Frontend-Streamlit-red?style=for-the-badge&logo=streamlit&logoColor=white)

## 🚨 The Problem
Modern Smart Cities and Government Offices are vulnerable. A single compromised IoT device (like a smart bulb or printer) can act as a gateway for attackers to breach critical infrastructure. Traditional firewalls are often too expensive or complex for local deployment.

## 💡 The Solution: Cyber-Rakshak
**Cyber-Rakshak** is an indigenous, AI-powered **Edge Security Node** designed to protect local networks. It doesn't just block attacks; it actively deceives hackers using **Generative AI Decoys**.

### 🚀 Key Features
* **🧠 AI Threat Detection:** Uses an **Isolation Forest** model to detect behavioral anomalies in real-time.
* **🎭 Active Deception:** Automatically generates and uploads **Fake Data** (decoy passwords/SQL dumps) to the attacker, wasting their time and resources.
* **⛔ Kernel Kill Switch:** A human-operated button that physically severs the connection at the OS level (using `iptables`/`netsh`).
* **🌍 Real-Time Threat Map:** Visualizes attack origins and targets on a live 3D globe.
* **📂 Forensic Logging:** Auto-generates "Top Secret" incident reports for legal and forensic analysis.

## 🛠️ Technology Stack
* **Frontend:** Streamlit (Python)
* **Backend:** Scapy (Packet Sniffing), Pandas (Data Processing)
* **AI Model:** Scikit-Learn (Isolation Forest)
* **Visualization:** Plotly Express & Graph Objects

## 📸 Screenshots
*(Add a screenshot of your dashboard here later)*

## ⚙️ Installation & Usage

1.  **Clone the Repository**
    ```bash
    git clone [https://github.com/your-username/cyber-rakshak.git](https://github.com/your-username/cyber-rakshak.git)
    cd cyber-rakshak
    ```

2.  **Install Dependencies**
    ```bash
    pip install -r requirements.txt
    ```

3.  **Run the Application**
    ```bash
    streamlit run app.py
    ```

## ⚠️ Disclaimer
This tool is a **Proof of Concept (PoC)** developed for educational purposes and hackathon demonstration. It simulates network attacks and defense mechanisms.

## 👥 Team Dimension Drifters
* **Lead Developer:** [Your Name]
* **UI/UX:** [Teammate Name]
* **Backend Logic:** [Teammate Name]

---
*Made with ❤️ in India for a Safer Digital Future.*
