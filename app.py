import streamlit as st
import random
import pandas as pd
import plotly.express as px
from datetime import datetime
from ai_prediction import predict_risk
from cost_optimizer import cost_advice
from streamlit_autorefresh import st_autorefresh
from ai_advisor import generate_advice
from cloudwatch_metrics import (
    get_cpu_usage,
    get_network_in,
    get_cpu_history,
    get_network_history
)
from openrouter_ai import (
    ask_ai,
    cost_optimizer_ai,
    auto_remediation_ai
)

st.set_page_config(
    page_title="CloudGuard AI",
    page_icon="☁️",
    layout="wide"
)

auto_refresh = st.sidebar.checkbox(
    "Enable Auto Refresh",
    value=False
)

if auto_refresh:
    st_autorefresh(interval=10000, key="refresh")

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

cpu = get_cpu_usage()

cpu_history = get_cpu_history()

cpu_df = pd.DataFrame([
    {
        "Time": item["Timestamp"],
        "CPU": item["Average"]
    }
    for item in cpu_history
])

# ADD BELOW THE CPU BLOCK

network_history = get_network_history()

network_df = pd.DataFrame([
    {
        "Time": item["Timestamp"],
        "Network": item["Average"] / 1024
    }
    for item in network_history
])

memory = df["Memory"].iloc[-1]

network = get_network_in()

risk = predict_risk(cpu, memory, network)

network_score = min(network, 100)

health_score = max(
    0,
    min(
        100,
        int(
            100 - (
                cpu * 0.4 +
                memory * 0.4 +
                network_score * 0.2
            )
        )
    )
)

# Metrics Section

col1, col2, col3 = st.columns(3)

with col1:
    st.metric("🖥 CPU Usage", f"{cpu}%")

with col2:
    st.metric("💾 Memory Usage", f"{memory}%")

with col3:
    st.metric("🌐 Network In (KB)", f"{network} KB")

st.divider()


st.subheader("🏥 System Health Score")

st.progress(int(health_score))

st.metric(
    "Health Score",
    f"{int(health_score)}/100"
)

st.subheader("📈 Real AWS CPU Trend")

fig_cpu = px.line(
    cpu_df,
    x="Time",
    y="CPU",
    title="AWS CloudWatch CPU Usage"
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


st.subheader("📈 Real AWS Network Trend")

fig_network = px.line(
    network_df,
    x="Time",
    y="Network",
    title="AWS CloudWatch Network Usage (KB)"
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

# Sidebar Risk Indicator

if risk == "HIGH RISK":
    st.sidebar.error("🔴 HIGH RISK")

elif risk == "MEDIUM RISK":
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

st.header("🤖 AI Analysis")

st.write(f"Risk Level: {risk}")

if risk == "HIGH RISK":
    st.error("High resource pressure detected.")
elif risk == "MEDIUM RISK":
    st.warning("Moderate resource pressure detected.")
else:
    st.success("Infrastructure operating normally.")

advice = generate_advice(cpu, memory, network)

st.subheader("🧠 AI Recommendation")
st.info(advice)

st.subheader("💰 AI Cost Optimization")

if st.button("Analyze Cloud Costs"):

    with st.spinner("Analyzing AWS costs..."):

        cost_result = cost_optimizer_ai(
            cpu,
            memory,
            network
        )

        st.success(cost_result)

st.subheader("🛠 AI Auto-Remediation Engine")

if st.button("Generate Recovery Plan"):

    with st.spinner("Generating recovery plan..."):

        recovery_plan = auto_remediation_ai(
            cpu,
            memory,
            network,
            risk
        )

        st.success(recovery_plan)

# AI Analysis

# Incident Simulator

st.subheader("🎭 Incident Simulator")

incident = st.selectbox(
    "Select Incident",
    [
        "High CPU Usage",
        "Memory Leak",
        "Network Spike",
        "DDoS Attack"
    ]
)

if st.button("Simulate Incident"):

    with st.spinner("Simulating incident..."):

        simulation = ask_ai(
            f"""
        You are CloudGuard AI.

        This is a SIMULATED TRAINING SCENARIO.

        The incident is hypothetical and does not represent the current metrics.

        Simulate a realistic AWS cloud incident: {incident}

        Project Context:
        - Monitoring AWS EC2 instances
        - Monitoring CloudWatch metrics
        - Using CloudGuard AI for analysis
        - Using AWS networking metrics

        Provide:

        ## Impact
        ## Root Cause
        ## Recovery Plan
        ## AWS Services Used
        ## Cloud Operations Recommendation

        Rules:
        - Never invent EC2 instance IDs.
        - Never invent resource names.
        - Never invent account IDs.
        - Never mention risk level.
        - Use only standard AWS services and capabilities.
        - Do not invent AWS features or product names.
        - Refer to AWS WAF as a Web Application Firewall.
        - Avoid mentioning OWASP unless specifically relevant.
        - Generate a generic incident response report suitable for demonstration purposes.
        - Do not invent IP addresses.
        - Do not invent AWS regions.
        - Do not invent timestamps.
        - Do not mention AWS regions unless explicitly provided.
        - Use generic AWS infrastructure descriptions.
        - Only use information explicitly provided.
        - Do not change the current risk level unless explicitly provided.
        - Do not invent metric values.
        - Keep recommendations aligned with the provided metrics.
        - Do not invent exact numbers or statistics.
        - Use terms like "high traffic volume", "elevated latency", "increased resource utilization".
        - Do not invent hostnames, domains, timestamps, users, or revenue figures.
        - Do not mention services unless they are relevant.
        - Avoid assuming systems are compromised.
        - Avoid recommending instance recreation unless absolutely necessary.
        - Prefer mitigation, monitoring, filtering, and scaling actions.
        - Keep the scenario generic.
        - Focus on EC2, CloudWatch, Auto Scaling, WAF, Shield, and networking.
        - Use bullet points.
        - Keep response under 250 words.
        """,
            cpu,
            memory,
            network,
            risk
        )

        st.success(f"Simulation Results: {incident}")
        st.info("⚠️ This is a simulated training scenario, not a real incident.")
        st.markdown(simulation)

        st.download_button(
            "📥 Download Incident Report",
            data=simulation,
            file_name="incident_report.txt",
            mime="text/plain"
        )

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

st.subheader("💬 Ask CloudGuard AI")

question = st.text_input(
    "Ask about your infrastructure",
    key="cloud_question"
)

if question:

    with st.spinner("CloudGuard AI is thinking..."):

        answer = ask_ai(
            question,
            cpu,
            memory,
            network,
            risk
        )

        st.success(answer)

with st.expander("🚨 AI Incident Summary"):

    if st.button("Generate Incident Summary"):

        incident = ask_ai(
            "Summarize the current infrastructure status in 3 bullet points",
            cpu,
            memory,
            network,
            risk
        )

        st.write(incident)

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

    if risk == "HIGH RISK":
        report += " Immediate investigation and scaling required."

    elif risk == "MEDIUM RISK":
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
    "CloudGuard AI v3.0 | Autonomous Cloud Operations Assistant | Developed by Jebarson"
)