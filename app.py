import streamlit as st
import pandas as pd
import backend
import time
import plotly.express as px

# --- PAGE SETUP ---
st.set_page_config(
    page_title="Cyber-Rakshak Command Center",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- VISUAL STYLING (Safe Mode) ---
st.markdown("""
    <style>
        .stApp {background-color: #0E1117;}
        div.stMetric {background-color: #262730; border: 1px solid #444; padding: 10px; border-radius: 8px;}
        h1, h2, h3 {color: #00FF41 !important; font-family: 'Courier New', monospace;}
        .reportview-container {margin-top: -2em;}
        .stDeployButton {display:none;}
        #MainMenu {visibility: hidden;}
    </style>
""", unsafe_allow_html=True)

# --- INITIALIZATION ---
if "data" not in st.session_state:
    st.session_state["data"] = pd.DataFrame(columns=["Timestamp", "Device", "Destination", "Protocol", "AI_Status", "Anomaly_Score", "Alert"])

# --- SIDEBAR ---
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/9662/9662234.png", width=100)
    st.title("CYBER-RAKSHAK")
    st.markdown("---")
    st.markdown("**STATUS:** <span style='color:#00FF41'>● SYSTEM ONLINE</span>", unsafe_allow_html=True)
    st.markdown("**MODE:** 🛡️ ACTIVE DEFENSE")
    st.markdown("---")
    
    # CONTROLS
    run_simulation = st.checkbox("🟢 ENABLE AI SCANNING", value=True)
    st.markdown("---")
    attack_btn = st.button("⚠️ SIMULATE IOT ATTACK", type="primary", help="Inject Malicious Payload")
    
    if attack_btn:
        st.toast("🚨 INTRUSION DETECTED! ISOLATING DEVICE...", icon="🔥")

# --- MAIN DASHBOARD LAYOUT ---
st.title("🛡️ IOT SECURITY WAR ROOM")

# Create a placeholder for the live dashboard
dashboard_placeholder = st.empty()

# --- MAIN LOOP ---
if run_simulation:
    # 1. FETCH DATA
    new_packet = backend.get_data_stream(num_packets=1)[0]
    
    # 2. INJECT ATTACK IF BUTTON PRESSED
    if attack_btn:
        new_packet = backend.generate_fake_attack()
    
    # 3. APPEND TO HISTORY
    # Convert single dict to DataFrame properly
    df_new = pd.DataFrame([new_packet])
    st.session_state["data"] = pd.concat([df_new, st.session_state["data"]], ignore_index=True).head(30) # Keep last 30
    
    df = st.session_state["data"]
    
    # 4. RENDER UI INSIDE PLACEHOLDER (Prevents flashing)
    with dashboard_placeholder.container():
        # --- METRICS ROW ---
        threats = df[df["AI_Status"] == "🚨 THREAT"]
        
        m1, m2, m3, m4 = st.columns(4)
        m1.metric("PACKETS SCANNED", f"{len(df) + 2450}", delta="120 pkts/s")
        m2.metric("SECURE TRAFFIC", "99.1%", delta="Stable", delta_color="normal")
        
        if not threats.empty:
            m3.metric("ACTIVE THREATS", f"{len(threats)}", delta="CRITICAL", delta_color="inverse")
            m4.metric("SYSTEM HEALTH", "COMPROMISED", delta="Action Req", delta_color="inverse")
        else:
            m3.metric("ACTIVE THREATS", "0", delta="None", delta_color="off")
            m4.metric("SYSTEM HEALTH", "SECURE", delta="Optimal", delta_color="normal")

        st.markdown("---")

        # --- SPLIT VIEW: MAP & GRAPHS ---
        col_left, col_right = st.columns([2, 1])
        
        with col_left:
            st.subheader("📝 LIVE PACKET INSPECTION")
            
            # Highlight Threats in Red
            def highlight_row(row):
                return ['background-color: #330000; color: #FF4B4B' if row['AI_Status'] == '🚨 THREAT' else '' for _ in row]

            st.dataframe(
                df[["Timestamp", "Device", "Destination", "Protocol", "AI_Status", "Alert"]].style.apply(highlight_row, axis=1),
                use_container_width=True,
                height=300
            )

        with col_right:
            st.subheader("📡 ANOMALY SCORE")
            if not df.empty:
                # Create a Line Chart
                fig = px.line(df, x="Timestamp", y="Anomaly_Score", markers=True, title="Isolation Forest Output")
                
                # Style the chart to look "Hacker-like"
                fig.update_layout(
                    paper_bgcolor="#111", 
                    plot_bgcolor="#111", 
                    font_color="#00FF41",
                    margin=dict(l=20, r=20, t=40, b=20),
                    height=300
                )
                
                # Make the line RED if there is a threat
                line_color = '#FF0000' if not threats.empty else '#00FF41'
                fig.update_traces(line_color=line_color, line_width=3)
                
                st.plotly_chart(fig, use_container_width=True)

    # 5. AUTO REFRESH RATE
    time.sleep(1.5) # Wait 1.5 seconds
    st.rerun()      # Restart loop