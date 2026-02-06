import streamlit as st
import pandas as pd
import backend
import alerts
import time
import plotly.express as px
import plotly.graph_objects as go
import random

# --- PAGE SETUP ---
st.set_page_config(
    page_title="Cyber-Rakshak Dashboard",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- CINEMATIC BOOT SEQUENCE ---
if "booted" not in st.session_state:
    with st.empty():
        st.write("Initializing UI...")
        bar = st.progress(0)
        time.sleep(0.5)
        st.session_state["booted"] = True
        st.rerun()

# --- MODERN UI STYLING (The "SaaS" Look) ---
st.markdown("""
    <style>
        /* MAIN BACKGROUND */
        .stApp {
            background-color: #0c0c0c; /* Deepest Black */
            font-family: 'Helvetica Neue', sans-serif;
        }

        /* CARD STYLE (The rounded boxes) */
        .css-card {
            background-color: #1a1a1a;
            border-radius: 15px;
            padding: 20px;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.3);
            margin-bottom: 20px;
            border: 1px solid #333;
        }

        /* METRICS STYLING */
        div[data-testid="stMetric"] {
            background-color: #262626;
            padding: 15px;
            border-radius: 12px;
            border-left: 5px solid #ccff00; /* Lime Accent */
            color: white;
        }
        div[data-testid="stMetricLabel"] {
            color: #b0b0b0;
            font-size: 0.85rem;
        }
        div[data-testid="stMetricValue"] {
            color: #ffffff;
            font-size: 1.8rem;
            font-weight: 700;
        }

        /* HEADERS */
        h1, h2, h3 {
            color: #ffffff !important;
            font-family: 'Helvetica Neue', sans-serif;
            font-weight: 700;
        }
        
        /* CUSTOM TABLE (Clean Look) */
        .modern-table {
            width: 100%;
            border-collapse: separate;
            border-spacing: 0 8px; /* Spacing between rows */
            color: #e0e0e0;
            font-size: 0.9rem;
        }
        .modern-table th {
            color: #888;
            font-weight: 600;
            text-align: left;
            padding: 10px 15px;
            border-bottom: 1px solid #333;
        }
        .modern-table td {
            background-color: #1a1a1a;
            padding: 12px 15px;
            border-top: 1px solid #333;
            border-bottom: 1px solid #333;
        }
        .modern-table tr td:first-child { border-top-left-radius: 10px; border-bottom-left-radius: 10px; border-left: 1px solid #333; }
        .modern-table tr td:last-child { border-top-right-radius: 10px; border-bottom-right-radius: 10px; border-right: 1px solid #333; }

        /* ALERT ROW STYLE */
        .alert-row td {
            background-color: #2d1a1a !important; /* Dark Red BG */
            color: #ff6b6b !important;
            border: 1px solid #ff4b4b;
        }
        
        /* SIDEBAR */
        section[data-testid="stSidebar"] {
            background-color: #111;
            border-right: 1px solid #333;
        }
        
        /* BUTTONS */
        .stButton button {
            border-radius: 8px;
            font-weight: 600;
        }
    </style>
""", unsafe_allow_html=True)

# --- INITIALIZATION ---
if "data" not in st.session_state:
    st.session_state["data"] = pd.DataFrame(columns=["Timestamp", "Device", "Destination", "Protocol", "AI_Status", "Anomaly_Score", "Alert"])

if "scan_results" not in st.session_state:
    st.session_state["scan_results"] = None

if "attack_data" not in st.session_state:
    st.session_state["attack_data"] = None

# --- SIDEBAR (Modern Icons) ---
with st.sidebar:
    st.image("https://img.icons8.com/fluency/96/shield.png", width=60)
    st.title("Cyber-Rakshak")
    st.caption("v2.0 PRO // DIMENSION DRIFTERS")
    st.markdown("---")
    
    st.markdown("### ⚙️ CONTROLS")
    run_simulation = st.checkbox("Active Monitoring", value=True)
    
    st.markdown("### ⚡ ACTIONS")
    # ATTACK BUTTON
    if st.button("⚠️ SIMULATE ATTACK", type="primary", use_container_width=True):
        new_packet = backend.generate_fake_attack()
        with st.spinner("Analyzing Traffic Patterns..."):
            counter_strike = backend.deploy_decoy_data(new_packet["Destination"])
            time.sleep(0.8)
        st.session_state["attack_data"] = {"packet": new_packet, "counter_strike": counter_strike}
        alerts.send_discord_alert(new_packet["Device"], new_packet["Destination"], new_packet["Anomaly_Score"])
        st.toast("Threat Detected", icon="🚨")

    # POST-ATTACK TOOLS
    if st.session_state["attack_data"]:
        st.markdown("---")
        st.markdown("### 🛡️ RESPONSE")
        
        attack_info = st.session_state["attack_data"]["packet"]
        
        # 1. Download Report
        report_text = f"CONFIDENTIAL REPORT\nTARGET: {attack_info['Destination']}\nTIME: {attack_info['Timestamp']}"
        st.download_button("📄 Download Forensic Log", report_text, file_name="forensic_log.txt", use_container_width=True)
        
        # 2. Kill Switch
        if st.button("⛔ ENGAGE KILL SWITCH", type="secondary", use_container_width=True):
            progress_bar = st.progress(0)
            status_text = st.empty()
            for i in range(50):
                time.sleep(0.01)
                progress_bar.progress(i*2)
            
            attacker_ip = st.session_state["attack_data"]["packet"]["Destination"]
            res = backend.sever_connection(attacker_ip)
            if res["status"] == "success": st.success("Target Blocked")
            else: st.warning("Simulation Blocked")
            
            time.sleep(2)
            st.session_state["attack_data"] = None
            st.rerun()
            
    st.markdown("---")
    
    # --- NETWORK SCANNER SECTION ---
    if st.button("🔍 Scan Network", use_container_width=True):
        # Trigger the scan and save to session state
        st.session_state["scan_results"] = backend.scan_network_devices()
        
    # DISPLAY RESULTS IF THEY EXIST
    if st.session_state["scan_results"] is not None:
        st.success(f"Found {len(st.session_state['scan_results'])} Devices")
        
        # Convert to DataFrame for cleaner display
        scan_df = pd.DataFrame(st.session_state["scan_results"])
        
        # Display just the important columns to save space
        if not scan_df.empty:
            st.dataframe(
                scan_df[["IP", "Status", "Type"]], 
                use_container_width=True, 
                hide_index=True
            )
        
        if st.button("❌ Clear Scan", use_container_width=True):
            st.session_state["scan_results"] = None
            st.rerun()

# --- MAIN DASHBOARD LAYOUT ---
st.title("🛡️ Command Center")

# --- TOP METRICS ROW (Card Style) ---
dashboard_placeholder = st.empty()

# --- MAIN LOOP ---
if run_simulation:
    # Traffic Logic
    if st.session_state["attack_data"] and random.random() < 0.6:
        new_packet = st.session_state["attack_data"]["packet"].copy()
        new_packet["Timestamp"] = time.strftime("%H:%M:%S")
        new_packet["AI_Status"] = "🚨 THREAT" 
    else:
        new_packet = backend.get_data_stream(num_packets=1)[0]
    
    # Update Data
    df_new = pd.DataFrame([new_packet])
    st.session_state["data"] = pd.concat([df_new, st.session_state["data"]], ignore_index=True).head(30)
    df = st.session_state["data"]
    
    with dashboard_placeholder.container():
        # --- ROW 1: METRICS ---
        c1, c2, c3, c4 = st.columns(4)
        if "total_packets" not in st.session_state: st.session_state["total_packets"] = 2450 
        st.session_state["total_packets"] += random.randint(50, 150)
        
        threats = df[df["AI_Status"] == "🚨 THREAT"]
        
        c1.metric("Network Load", f"{st.session_state['total_packets']:,}", "+120/s")
        c2.metric("Secure Traffic", "99.1%", "Stable")
        
        if not threats.empty:
            c3.metric("Active Threats", f"{len(threats)}", "CRITICAL", delta_color="inverse")
            c4.metric("System Status", "COMPROMISED", "Action Req", delta_color="inverse")
        else:
            c3.metric("Active Threats", "0", "None", delta_color="off")
            c4.metric("System Status", "SECURE", "Optimal")

        # --- ROW 2: MAP & ATTACK DETAILS ---
        col_map, col_details = st.columns([2, 1])
        
        with col_map:
            st.markdown('<div class="css-card">', unsafe_allow_html=True)
            st.subheader("🌍 Real-Time Threat Tracer")
            
            # --- MAP LOGIC ---
            start_lat, start_lon = 20.5937, 78.9629  # India
            
            fig = go.Figure()
            
            # Only draw the RED LINE if there is an active attack
            if st.session_state["attack_data"]:
                end_lat, end_lon = 39.9042, 116.4074 # Beijing (Target)
                
                # 1. The Line
                fig.add_trace(go.Scattergeo(
                    lat = [start_lat, end_lat], lon = [start_lon, end_lon],
                    mode = 'lines', line = dict(width = 2, color = '#ff4b4b'), opacity = 0.8
                ))
                # 2. The Target Dot
                fig.add_trace(go.Scattergeo(
                    lat = [end_lat], lon = [end_lon],
                    mode = 'markers', marker = dict(size = 20, color = '#ff4b4b', opacity=0.3), hoverinfo='none'
                ))
                # 3. Text Labels
                fig.add_trace(go.Scattergeo(
                    lat = [start_lat, end_lat], lon = [start_lon, end_lon],
                    mode = 'markers+text',
                    marker = dict(size = 8, color = '#ffffff'),
                    text = ["You", "⚠️ ATTACKER"], textposition="top center",
                    textfont = dict(color="white", size=10, family="Helvetica")
                ))
            else:
                # SAFE STATE: Just show "You"
                fig.add_trace(go.Scattergeo(
                    lat = [start_lat], lon = [start_lon],
                    mode = 'markers+text',
                    marker = dict(size = 10, color = '#ccff00'), # Green dot
                    text = ["🛡️ You (Secure)"], textposition="top center",
                    textfont = dict(color="#ccff00", size=11, family="Helvetica")
                ))

            # --- MAP STYLING (REMOVED WHITE BOX) ---
            fig.update_layout(
                geo = dict(
                    projection_type = "equirectangular",
                    showland = True, landcolor = "#262626",
                    showocean = True, oceancolor = "#1a1a1a", # Matches Card BG
                    showcountries = True, countrycolor = "#444",
                    showcoastlines = False,
                    bgcolor = "#1a1a1a" # Matches Card BG
                ),
                margin = dict(l=0, r=0, t=10, b=0),
                paper_bgcolor = "#1a1a1a", # Matches Card BG
                plot_bgcolor = "#1a1a1a",
                height = 300,
                showlegend = False
            )
            st.plotly_chart(fig, use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)

        with col_details:
            if st.session_state["attack_data"]:
                data = st.session_state["attack_data"]
                cs = data["counter_strike"]
                st.markdown('<div class="css-card" style="border: 1px solid #ff4b4b;">', unsafe_allow_html=True)
                st.subheader("🚨 Threat Intelligence")
                st.write(f"**Target:** {cs['target']}")
                st.write(f"**Payload:** {cs['filename']}")
                st.code(cs['payload'][:100] + "...", language="sql")
                st.markdown("</div>", unsafe_allow_html=True)
            else:
                st.markdown('<div class="css-card">', unsafe_allow_html=True)
                st.subheader("✅ System Diagnostics")
                st.write("Firewall: **Active**")
                st.write("IPS Engine: **Running**")
                st.write("Last Scan: **Just Now**")
                st.progress(100)
                st.markdown("</div>", unsafe_allow_html=True)

        # --- ROW 3: TABLE & GRAPH ---
        col_table, col_graph = st.columns([2, 1])
        
        with col_table:
            st.markdown("### 📝 Live Traffic")
            # Custom HTML Table
            display_df = df[["Timestamp", "Device", "Destination", "Protocol", "AI_Status"]]
            html_rows = []
            for row in display_df.to_dict('records'):
                row_class = "alert-row" if row['AI_Status'] == "🚨 THREAT" else ""
                cells = "".join([f"<td>{val}</td>" for val in row.values()])
                html_rows.append(f"<tr class='{row_class}'>{cells}</tr>")
            
            final_html = f"""
            <div class="css-card" style="padding:10px;">
            <table class='modern-table'>
                <thead><tr><th>TIME</th><th>DEVICE</th><th>DEST</th><th>PROTO</th><th>STATUS</th></tr></thead>
                <tbody>{''.join(html_rows)}</tbody>
            </table>
            </div>
            """
            st.markdown(final_html, unsafe_allow_html=True)

        with col_graph:
            st.markdown("### 📈 Anomaly Score")
            if not df.empty:
                fig_graph = px.line(df, x="Timestamp", y="Anomaly_Score")
                fig_graph.update_layout(
                    paper_bgcolor="rgba(0,0,0,0)",
                    plot_bgcolor="rgba(0,0,0,0)",
                    font_color="#888",
                    margin=dict(l=10, r=10, t=10, b=10),
                    height=250,
                    xaxis=dict(showgrid=False),
                    yaxis=dict(showgrid=True, gridcolor="#333")
                )
                line_color = '#ff4b4b' if not threats.empty else '#ccff00'
                fig_graph.update_traces(line_color=line_color, line_width=3, fill='tozeroy', fillcolor=f"rgba({255 if not threats.empty else 204}, {75 if not threats.empty else 255}, 0, 0.1)")
                
                st.markdown('<div class="css-card">', unsafe_allow_html=True)
                st.plotly_chart(fig_graph, use_container_width=True)
                st.markdown('</div>', unsafe_allow_html=True)

    time.sleep(1.5)
    st.rerun()
