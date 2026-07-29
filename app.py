import re
import streamlit as st
import random
import time
import pandas as pd
import plotly.express as px
from datetime import datetime
from streamlit_autorefresh import st_autorefresh
from ai_advisor import generate_advice
from aws_cloudwatch import create_cpu_alarm
from email_service import send_email
from aws_ses import send_email
from report_generator import generate_report
from cost_optimizer import cost_advice
from metric_logger import save_metrics
from predict import predict_future_cpu
from detect_anomaly import detect_anomaly
from failure_predict import predict_failure
from real_metric_logger import save_real_metrics

from agents.orchestrator import run_workflow

from aws_cost import (
    get_cost_summary,
    get_cost_by_service
)

from aws_ec2 import (
    get_instance_status,
    start_instance,
    stop_instance,
    reboot_instance,
    get_instance_details
)

from activity_logger import (
    log_activity,
    get_logs
)

from aws_cloudwatch import (
    create_cpu_alarm,
    list_alarms,
    delete_alarm,
    get_alarm_status
)

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

st.markdown("""
<style>

button[data-baseweb="tab"]{
    background-color:#1e1e1e;
    border-radius:12px;
    padding:18px 28px;
    font-size:18px;
    font-weight:700;
    color:white;
    margin-right:12px;
}

button[data-baseweb="tab"][aria-selected="true"]{
    background-color:#0E76FD;
    color:white;
}

div[data-baseweb="tab-list"]{
    gap:15px;
}

</style>
""", unsafe_allow_html=True)

auto_refresh = st.sidebar.checkbox(
    "Enable Auto Refresh",
    value=False
)

if auto_refresh:
    st_autorefresh(interval=10000, key="refresh")

# Sidebar
st.sidebar.image(
    "https://img.icons8.com/fluency/96/cloud.png",
    width=80
)

st.sidebar.title("CloudGuard AI")
st.sidebar.caption("Autonomous Cloud Operations Platform")

st.sidebar.info("""
Cloud Operations Dashboard

Version: 4.0
Status: Active
""")

st.sidebar.write("🕒 Current Time")
st.sidebar.write(datetime.now().strftime("%d-%m-%Y %H:%M:%S"))

st.sidebar.metric(
    "System Uptime",
    "99.9%"
)

# Title

st.markdown(
    """
    <h1 style='text-align: center;'>
        ☁ CloudGuard AI
    </h1>

    <h4 style='text-align: center; color: #CFCFCF;'>
        Real-Time AWS Cloud Operations Dashboard
    </h4>
    """,
    unsafe_allow_html=True
)

left, center, right = st.columns([1, 8, 1])

with center:

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.success("🟢 AWS Connected")

    with col2:
        st.info("🖥 EC2")

    with col3:
        st.warning("🚨 Alarm")

    with col4:
        st.success("💰 AWS Cost")

st.divider()

tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "📊 Dashboard",
    "☁ Infrastructure",
    "🧠 AI Insights",
    "💰 Cost",
    "📄 Reports"
])

workflow = run_workflow()

prediction = workflow["prediction"]

metrics = workflow["metrics"]
reasoning = workflow["reasoning"]
diagnosis = workflow["diagnosis"]
plan = workflow["plan"]
approval = workflow["approval"]
action = workflow["action"]
report = workflow["report"]

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

cpu = metrics["cpu"]
memory = metrics["memory"]
network = metrics["network"]

cpu_history = metrics["cpu_history"]
network_history = metrics["network_history"]

cpu_df = pd.DataFrame([
    {
        "Time": item["Timestamp"],
        "CPU": item["Average"]
    }
    for item in cpu_history
])

network_df = pd.DataFrame([
    {
        "Time": item["Timestamp"],
        "Network": item["Average"] / 1024
    }
    for item in network_history
])

risk = metrics["risk"]

if risk == "HIGH RISK":
    st.sidebar.error("🔴 HIGH RISK")

elif risk == "MEDIUM RISK":
    st.sidebar.warning("🟡 MEDIUM RISK")

else:
    st.sidebar.success("🟢 LOW RISK")

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

# predicted_cpu = predict_cpu(
#     cpu,
#     memory,
#     network,
#     metrics.get("disk", 0),
#     health_score
# )

save_metrics(metrics, health_score)

save_real_metrics(metrics, health_score)

future_cpu = predict_future_cpu(
    cpu,
    memory,
    network,
    metrics.get("disk", 0),
    health_score
)

anomaly = detect_anomaly(
    cpu,
    memory,
    network,
    metrics.get("disk", 0),
    health_score
)

failure_probability = predict_failure(
    cpu,
    memory,
    network,
    metrics.get("disk", 0),
    health_score
)

INSTANCE_ID = "i-0a281c83a51f3a6c4"

with tab1:

# Metrics Section

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric(
            "🖥 CPU Usage",
            f"{cpu:.2f} %",
            delta=f"{cpu-50:.1f}%"
        )

    with col2:
        st.metric(
            "💾 Memory",
            f"{memory:.2f} %",
            delta=f"{memory-50:.1f}%"
        )

    with col3:
        st.metric("🌐 Network In (KB)", f"{network} KB")

    with col4:
        st.metric("❤️ Health", f"{health_score}/100")

    if risk == "LOW RISK":
        st.subheader("🟢 Infrastructure Status")

        st.success(
            "All monitored AWS resources are operating normally."
        )

    elif risk == "MEDIUM RISK":
        st.warning("🟡 Infrastructure Status: Warning")

    else:
        st.error("🔴 Infrastructure Status: Critical")

    st.divider()

    st.caption(
        "Real-time metrics collected directly from AWS CloudWatch."
    )

    st.subheader("📈 Performance Trends")
    st.caption("Historical CloudWatch metrics for the monitored EC2 instance.")

    graph1, graph2 = st.columns(2)

    with graph1:

        st.subheader("📈 AWS EC2 CPU Utilization")

        if cpu_df.empty:
            st.info("Waiting for CloudWatch CPU metrics... Please wait 5-10 minutes after launching the EC2 instance.")
        else:
            fig_cpu = px.line(
                cpu_df,
                x="Time",
                y="CPU",
                title="CPU Utilization (%)"
            )

            st.plotly_chart(
                fig_cpu,
                width="stretch"
            )

    with graph2:

        st.subheader("📡 AWS Network Usage")

        if network_df.empty:
            st.info("Waiting for CloudWatch Network metrics... Please wait a few minutes.")
        else:
            fig_network = px.line(
                network_df,
                x="Time",
                y="Network",
                title="Network Traffic (KB)"
            )

            st.plotly_chart(
                fig_network,
                width="stretch"
            )

    # if "alerts" not in st.session_state:
    #     st.session_state.alerts = []

with tab2:

    st.subheader("🚨 AWS Infrastructure Health")
    st.write(
        "Monitor the real-time health of your AWS infrastructure using CloudWatch and EC2."
    )

    result = workflow["anomaly"]

    if result["status"] == "anomaly":

        st.error("🚨 Infrastructure Issue Detected")

    else:

        st.success("✅ Infrastructure Healthy")

    st.subheader("📋 Health Summary")

    col1, col2 = st.columns(2)

    with col1:

        st.metric(
            "CPU Usage",
            f"{metrics['cpu']} %"
        )   

        st.metric(
            "Network In",
            f"{metrics['network']} KB"
        )

    with col2:

        st.metric(
            "Network Out",
            f"{metrics['network_out']} KB"
        )

    if metrics["status_check"] == 0:

        st.success("✔ All EC2 Status Checks Passed")

    else:

        st.error(
            f"❌ {metrics['status_check']} Status Check(s) Failed"
        )

    alarms = get_alarm_status()

    if alarms:

        alarm = alarms[0]

        if alarm["state"] == "OK":

            st.success("🚨 CloudWatch Alarm : OK")

        elif alarm["state"] == "ALARM":

            st.error("🚨 CloudWatch Alarm : ALARM")

        else:

            st.warning(
                f"🚨 CloudWatch Alarm : {alarm['state']}"
            )

    st.divider()

    status = get_instance_status(INSTANCE_ID)

    details = get_instance_details(INSTANCE_ID)

    st.subheader("🖥 EC2 Information")

    info1, info2 = st.columns(2)

    with info1:

        st.write("**Name:**", details["Name"])

        st.write("**Instance ID:**", details["InstanceId"])

        st.write("**State:**", details["State"])

        st.write("**Instance Type:**", details["InstanceType"])

    with info2:

        st.write("**Public IP:**", details["PublicIP"])

        st.write("**Launch Time:**", details["LaunchTime"])

        st.write("**Region:**", details["Region"])

    st.subheader("🖥 EC2 Instance Control")

    st.metric(
        "EC2 Status",
        status.upper()
    )

    if status == "running":
        st.success("🟢 Instance Healthy")

    elif status == "stopped":
        st.error("🔴 Instance Offline")

    else:
        st.warning(f"🟡 Current State: {status.upper()}")

    st.caption(
        f"Last Updated: {datetime.now().strftime('%d-%m-%Y %H:%M:%S')}"
    )

    col1, col2, col3 = st.columns(3)

    with col1:

        if st.button(
            "▶️ Start EC2",
            use_container_width=True,
            disabled=(status == "running")
        ):

            with st.spinner("Starting EC2 Instance..."):

                start_instance(INSTANCE_ID)

                time.sleep(5)

            st.success("EC2 started successfully!")

            send_email(

                receiver="jebarson696@gmail.com",

                subject="CloudGuard AI - EC2 Started",

                body=f"""
            CloudGuard AI Notification

            Action:
            Start EC2

            Status:
            Success

            Instance:
            {INSTANCE_ID}

            Time:
            {datetime.now().strftime("%d-%m-%Y %H:%M:%S")}
            """

            )

            log_activity(
                "Start EC2",
                "Success"
            )

            st.rerun()

    with col2:

        with st.popover("⏹ Stop EC2", use_container_width=True):

            st.error("⚠️ Confirm Stop")

            st.write(
                "Stop this EC2 instance?"
            )

            if st.button(
                "✅ Confirm Stop",
                use_container_width=True
            ):

                with st.spinner(
                    "Stopping EC2..."
                ):

                    stop_instance(INSTANCE_ID)

                    time.sleep(5)

                st.success(
                    "EC2 stopped successfully!"
                )

                send_email(

                    receiver="jebarson696@gmail.com",

                    subject="CloudGuard AI - EC2 Stopped",

                    body=f"""
                CloudGuard AI Notification

                Action:
                Stop EC2

                Status:
                Success

                Instance:
                {INSTANCE_ID}

                Time:
                {datetime.now().strftime("%d-%m-%Y %H:%M:%S")}
                """

                )

                log_activity(
                    "Stop EC2",
                    "Success"
                )

                st.rerun()

    with col3:

        with st.popover("🔄 Reboot EC2", use_container_width=True):

            st.warning("⚠️ Confirm Reboot")

            st.write(
                "Restart this EC2 instance?"
            )

            if st.button(
                "✅ Confirm Reboot",
                use_container_width=True
            ):

                with st.spinner(
                    "Rebooting EC2..."
                ):

                    reboot_instance(INSTANCE_ID)

                    time.sleep(5)

                st.success(
                    "EC2 rebooted successfully!"
                )

                send_email(

                    receiver="jebarson696@gmail.com",

                    subject="CloudGuard AI - EC2 Rebooted",

                    body=f"""
                CloudGuard AI Notification

                Action:
                Reboot EC2

                Status:
                Success

                Instance:
                {INSTANCE_ID}

                Time:
                {datetime.now().strftime("%d-%m-%Y %H:%M:%S")}
                """

                )

                send_email(
                    subject=f"CloudGuard AI - {action}",
                    body=f"""
                Time: {datetime.now()}

                Action: {action}

                Status: {status}

                Risk Level: {risk}

                CPU: {cpu}%

                Memory: {memory}%

                Network: {network} KB

                Instance ID: {INSTANCE_ID}
                """,
                    receiver="jebarson696@gmail.com"
                )

                log_activity(
                    "Reboot EC2",
                    "Success"
                )

                st.rerun()

    st.divider()

    st.subheader("🚨 CloudWatch Alarm Management")

    if st.button("🔄 Refresh Alarms"):
        st.rerun()

    alarm_name = st.text_input(
        "Alarm Name",
        value="CloudGuard-HighCPU"
    )

    threshold = st.slider(
        "CPU Alarm Threshold (%)",
        min_value=50,
        max_value=100,
        value=80
    )

    if st.button(
        "🚨 Create CPU Alarm",
        use_container_width=True
    ):

        with st.spinner("Creating CloudWatch Alarm..."):

            create_cpu_alarm(
                INSTANCE_ID,
                alarm_name,
                threshold
            )

        st.success("CloudWatch Alarm Created!")

        send_email(

            receiver="jebarson696@gmail.com",

            subject="CloudGuard AI - CloudWatch Alarm Created",

            body=f"""
    CloudGuard AI Notification

    Action:
    Create CloudWatch Alarm

    Status:
    Success

    Threshold:
    {threshold}%

    Time:
    {datetime.now().strftime("%d-%m-%Y %H:%M:%S")}
    """
        )

        log_activity(
            "Create CPU Alarm",
            "Success"
        )

    st.divider()

    st.subheader("📋 Existing CloudWatch Alarms")

    alarms = list_alarms()

    if alarms:

        for alarm in alarms:

            st.success(f"""
            ### 🔔 {alarm['AlarmName']}

            Status: {alarm['StateValue']}

            Threshold:
            {alarm['Threshold']} %

            Metric:
            {alarm['MetricName']}
            """)

    else:

        st.info("No CloudWatch Alarms Found.")

    alarm_names = [
        alarm["AlarmName"]
        for alarm in alarms
    ]

    if alarm_names:

        selected_alarm = st.selectbox(
            "Select Alarm",
            alarm_names
        )

        if st.button(
            "🗑 Delete Selected Alarm",
            use_container_width=True
        ):

            delete_alarm(selected_alarm)

            st.success("Alarm Deleted!")

            log_activity(
                "Delete Alarm",
                "Success"
            )

            st.rerun()

    st.subheader("📊 Real CloudWatch Alarm Status")

    alarms = get_alarm_status()

    if alarms:

        for alarm in alarms:

            col1, col2 = st.columns([3, 1])

            with col1:

                st.markdown(f"### 🚨 {alarm['name']}")

                st.write(f"**Last Updated:** {alarm['updated']}")

            with col2:

                if alarm["state"] == "OK":

                    st.success("🟢 OK")

                    st.info("Infrastructure Healthy")

                elif alarm["state"] == "ALARM":

                    st.error("🔴 ALARM")

                    st.warning("Immediate Attention Required")

                else:

                    st.warning("🟡 INSUFFICIENT DATA")

        with st.expander("View Alarm Details"):

            st.write(alarm["reason"])

        st.divider()

    else:

        st.info("No CloudWatch alarms found.")
    



with tab3:

    st.subheader("🧠 AI Insights")

    st.subheader("⚠️ Risk Level")

    if risk == "HIGH RISK":
        st.error("🔴 HIGH RISK")

    elif risk == "MEDIUM RISK":
        st.warning("🟡 MEDIUM RISK")

    else:
        st.success("🟢 LOW RISK")

    st.subheader("🤖 AI Predictive Failure Detection")

    st.metric(
        "🔮 Predicted CPU (Next Interval)",
        f"{future_cpu:.2f}%"
    )

    if future_cpu > 80:
        st.error("⚠️ High CPU usage predicted.")
    elif future_cpu > 60:
        st.warning("🟡 Moderate CPU usage predicted.")
    else:
        st.success("🟢 CPU usage is predicted to remain stable.")

    st.subheader("🚨 AI Anomaly Detection")

    if anomaly == -1:
        st.error("🔴 Anomaly detected! The current system behaviour is unusual.")
    else:
        st.success("🟢 System behaviour is normal.")

    st.subheader("⚠️ AI Failure Probability")

    st.metric(
        "Failure Probability",
        f"{failure_probability:.1f}%"
    )

    if failure_probability > 80:
        st.error("🔴 High risk of system failure predicted.")
    elif failure_probability > 50:
        st.warning("🟡 Moderate risk of failure. Continue monitoring.")
    else:
        st.success("🟢 Low risk of failure.")

    st.subheader("🩺 AI Diagnosis")
    st.info(diagnosis)

    st.divider()


    st.subheader("📋 Recovery Plan")

    for step in workflow["plan"]:
        st.write(step)

    if "approved" not in st.session_state:
        st.session_state.approved = False

    if approval["required"]:

        if not st.session_state.approved:

            if st.button("✅ Approve Action", width="stretch"):

                before_cpu = cpu
                before_memory = memory
                before_network = network

                with st.spinner("Executing approved action..."):

                    if action["action"] == "Reboot EC2":

                        reboot_instance(INSTANCE_ID)

                        time.sleep(30)

                        new_cpu = get_cpu_usage()
                        new_network = get_network_in()

                        st.subheader("📊 Recovery Verification")

                        col1, col2 = st.columns(2)

                        with col1:
                            st.metric(
                                "CPU Before",
                                f"{before_cpu}%"
                            )

                        with col2:
                            st.metric(
                                "CPU After",
                                f"{new_cpu}%"
                            )

                    elif action["action"] == "Stop EC2":

                        stop_instance(INSTANCE_ID)

                    elif action["action"] == "Start EC2":

                        start_instance(INSTANCE_ID)

                    elif action["action"] == "Monitor":

                        st.info("Infrastructure is healthy.")

                    elif action["action"] == "Create CloudWatch Alarm":

                        create_cpu_alarm(INSTANCE_ID)

                    time.sleep(5)

                st.success("Action executed successfully!")

                st.rerun()



with tab4:

    st.subheader("💰 AWS Cost Optimization")
    summary = get_cost_summary()
    services = get_cost_by_service()
    st.caption("Analyze AWS resource usage and identify cost-saving opportunities.")

    col1, col2 = st.columns(2)

    with col1:

        st.metric(
            "Current Month Cost",
            f"${summary['cost']:.2f}"
        )

    with col2:

        status = "Estimated" if summary["estimated"] else "Final"

        st.metric(
            "Billing Status",
            status
        )

    st.subheader("📊 Cost by AWS Service")

    paid_services = [
        s for s in services
        if s["cost"] > 0
    ]

    if paid_services:

        for service in paid_services:

            col1, col2 = st.columns([4, 1])

            with col1:
                st.write(service["service"])

            with col2:
                st.write(f"${service['cost']:.2f}")

    else:

        st.info(
            "No billable AWS services detected this month.\n\n"
            "Your account is currently operating within the AWS Free Tier "
            "or has no billable usage."
        )

    if services:

        paid_services = [s for s in services if s["cost"] > 0]

        st.subheader("🏆 Highest Cost Service")

        if paid_services:

            highest = max(
                paid_services,
                key=lambda x: x["cost"]
            )

            st.success(
                f"{highest['service']} (${highest['cost']:.2f})"
            )

        else:

            st.info(
                "No billable AWS services detected this month."
            )

    st.subheader("🤖 AI Cost Recommendation")

    if summary["cost"] == 0:

        st.info("""
    ### Status

    ✅ **Operating within the AWS Free Tier**

    ### Recommendations

    • No immediate cost optimization is required.

    • Continue monitoring AWS usage.

    • Review monthly costs regularly.
    """)

    else:

        cost_result = cost_optimizer_ai(
            cpu,
            memory,
            network,
            summary["cost"]
        )

        with st.expander(
            "View AI Cost Recommendation",
            expanded=True
        ):
            st.markdown(cost_result)

    st.divider()




with tab5:

    st.subheader("📝 Cloud Operations Activity Log")

    logs = get_logs()

    if logs:

        df = pd.DataFrame(logs[::-1])

        st.dataframe(
            df,
            width="stretch",
            hide_index=True
        )

    else:

        st.info("No cloud operations have been recorded yet.")

    st.subheader("🏗️ System Architecture")

    with st.expander("View CloudGuard AI Architecture", expanded=False):

        st.markdown("""
    ```text
                        ☁ CloudGuard AI
            Real-Time AWS Cloud Operations Platform
    ════════════════════════════════════════════════════════════

                    AWS Cloud Infrastructure
                            │
         ┌──────────────────┼──────────────────┐
         ▼                  ▼                  ▼
    Amazon EC2        CloudWatch        Cost Explorer
         │                  │                  │
         └──────────────────┼──────────────────┘
                            ▼
            CloudGuard AI Intelligence Engine
                            │
         ┌──────────────────┼──────────────────┐
         ▼                  ▼                  ▼
 Infrastructure     AI Diagnosis     Cost Optimization
    Analysis
                            │
                            ▼
                   Recovery Planning
                            │
                            ▼
                  AWS Action Manager
                            │
       ┌──────────────┬──────────────┬──────────────┐
       ▼              ▼              ▼
  Start/Stop     Alarm Manager    SES Email Alerts
  Reboot EC2
       │
       └──────────────┬──────────────┘
                      ▼
          Activity Logs & Health Reports

""")

    st.subheader("📄 Generate Infrastructure Report")

    st.caption(
        "Generate a downloadable report summarizing the current AWS infrastructure status."
    )

    if st.button("📄 Generate Health Report"):

        report = generate_report(
            metrics,
            action
        )

        with st.expander("📄 Preview Report", expanded=True):
            st.text(report)

        st.download_button(
            "📥 Download Report",
            report,
            file_name="cloudguard_report.txt"
        )

    st.divider()

    st.caption(
        "CloudGuard AI v3.0 • Real-Time AWS Cloud Operations Dashboard • Developed by Jebarson"
    )