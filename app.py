import streamlit as st
import random
import pandas as pd
import plotly.express as px
from datetime import datetime
from streamlit_autorefresh import st_autorefresh

st.set_page_config(
page_title="CloudGuard AI",
page_icon="☁️",
layout="wide"
)

st_autorefresh(interval=5000, key="refresh")

# Sidebar
st.sidebar.title("☁️ CloudGuard AI")

st.sidebar.info("""
Cloud Operations Dashboard

Version: 3.0
Status: Active
""")

st.sidebar.write("🕒 Current Time")
st.sidebar.write(datetime.now().strftime("%d-%m-%Y %H:%M:%S"))

st.sidebar.write("⏱ Uptime")
st.sidebar.success("99.9%")

# Title

st.title("☁️ CloudGuard AI")
st.subheader("Autonomous Cloud Operations Assistant")

# Generate Metrics

history = []

for i in range(20):
    history.append({
        "Time": i,
        "CPU": random.randint(20, 100),
        "Memory": random.randint(30, 100),
        "Network": random.randint(10, 100)
    })

df = pd.DataFrame(history)

cpu = df["CPU"].iloc[-1]
memory = df["Memory"].iloc[-1]
network = df["Network"].iloc[-1]

health_score = max(
    0,
    min(
        100,
        int(100 - ((cpu * 0.4) + (memory * 0.4) + (network * 0.2)))
    )
)

# Metrics Section

col1, col2, col3 = st.columns(3)

with col1:
    st.metric("🖥 CPU Usage", f"{cpu}%")

with col2:
    st.metric("💾 Memory Usage", f"{memory}%")

with col3:
    st.metric("🌐 Network Usage", f"{network}%")

st.divider()


st.subheader("🏥 System Health Score")

st.progress(int(health_score))

st.metric(
    "Health Score",
    f"{int(health_score)}/100"
)

st.subheader("📈 CPU Trend")

fig_cpu = px.line(
    df,
    x="Time",
    y="CPU",
    title="CPU Usage Trend"
)

st.plotly_chart(fig_cpu, use_container_width=True)

st.subheader("📈 Memory Trend")

fig_memory = px.line(
    df,
    x="Time",
    y="Memory",
    title="Memory Usage Trend"
)

st.plotly_chart(fig_memory, use_container_width=True)


st.subheader("📈 Network Trend")

fig_network = px.line(
    df,
    x="Time",
    y="Network",
    title="Network Usage Trend"
)

st.plotly_chart(fig_network, use_container_width=True)

st.subheader("🥧 Resource Distribution")

pie_df = pd.DataFrame({
    "Resource": ["CPU", "Memory", "Network"],
    "Usage": [cpu, memory, network]
})

pie_chart = px.pie(
    pie_df,
    names="Resource",
    values="Usage",
    title="Current Resource Usage"
)

st.plotly_chart(pie_chart, use_container_width=True)

if "alerts" not in st.session_state:
    st.session_state.alerts = []

st.subheader("🖥 Server Status")

if health_score > 70:
    st.success("Server Status: Healthy")

elif health_score > 40:
    st.warning("Server Status: Moderate Load")

else:
    st.error("Server Status: Critical")

# Risk Analysis

if cpu > 85:
    risk = "HIGH"
    st.error("🚨 High CPU Usage Detected")

elif cpu > 60:
    risk = "MEDIUM"
    st.warning("⚠ Moderate Resource Usage")

else:
    risk = "LOW"
    st.success("✅ System Healthy")

if risk == "HIGH":
    alert = f"{datetime.now().strftime('%H:%M:%S')} - HIGH CPU ALERT"

    if alert not in st.session_state.alerts:
        st.session_state.alerts.append(alert)

# Sidebar Risk Indicator

if risk == "HIGH":
    st.sidebar.error("🔴 HIGH RISK")

elif risk == "MEDIUM":
    st.sidebar.warning("🟡 MEDIUM RISK")

else:
    st.sidebar.success("🟢 LOW RISK")

st.divider()

col1, col2, col3 = st.columns(3)

with col1:
    st.info(f"Average CPU: {round(df['CPU'].mean(),1)}%")

with col2:
    st.info(f"Average Memory: {round(df['Memory'].mean(),1)}%")

with col3:
    st.info(f"Average Network: {round(df['Network'].mean(),1)}%")

def ai_decision(cpu, memory, network):

    if cpu > 85:
        return {
            "risk": "HIGH",
            "cause": "High application load detected.",
            "action": "Scale resources and investigate running processes."
        }

    elif memory > 80:
        return {
            "risk": "MEDIUM",
            "cause": "Memory usage approaching critical level.",
            "action": "Review memory-intensive services."
        }

    else:
        return {
            "risk": "LOW",
            "cause": "Infrastructure operating normally.",
            "action": "Continue monitoring."
        }

analysis = ai_decision(cpu, memory, network)

# AI Analysis

st.header("🤖 AI Analysis")

if analysis["risk"] == "HIGH":
    st.error("🔴 HIGH RISK")

elif analysis["risk"] == "MEDIUM":
    st.warning("🟡 MEDIUM RISK")

else:
    st.success("🟢 LOW RISK")

st.write("### Root Cause")
st.write(analysis["cause"])

st.write("### Recommended Action")
st.write(analysis["action"])

st.header("🔮 Prediction")

if cpu > 80:
    st.error("CPU usage may reach critical levels soon.")

elif memory > 80:
    st.warning("Memory usage trend indicates potential resource exhaustion.")

else:
    st.success("No critical issues predicted.")

st.subheader("📋 Top Recommendations")

recommendations = [
    "Monitor CPU usage regularly",
    "Review application logs",
    "Optimize memory usage",
    "Enable auto-scaling policies"
]

for rec in recommendations:
    st.write("✅", rec)

st.divider()

# Alert History

st.subheader("🚨 Alert History")

if len(st.session_state.alerts) == 0:
    st.info("No alerts generated yet.")

else:
    for alert in reversed(st.session_state.alerts[-5:]):
        st.warning(alert)

st.divider()

if st.button("Generate Report"):

    report = f"""
Incident Report
-------------------------
Time: {datetime.now()}

CPU Usage: {cpu}%
Memory Usage: {memory}%
Network Usage: {network}%

Risk Level: {risk}

AI Summary:
CloudGuard AI analyzed current infrastructure metrics and generated this report.

Recommended Action:
"""

    if risk == "HIGH":
        report += " Immediate investigation and scaling required."

    elif risk == "MEDIUM":
        report += " Monitor system and review logs."

    else:
        report += " No action required."

    st.code(report)

    st.download_button(
        label="📥 Download Report",
        data=report,
        file_name="cloudguard_report.txt",
        mime="text/plain"
    )

st.divider()

st.caption(
    "CloudGuard AI v2.0 | Autonomous Cloud Operations Assistant | Developed by Jebarson"
)
