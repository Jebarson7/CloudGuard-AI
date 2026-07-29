from cloudwatch_metrics import (
    get_cpu_usage,
    get_network_in,
    get_network_out,
    get_status_check,
    get_cpu_history,
    get_network_history
)

from aws_ec2 import get_instance_status
import streamlit as st

INSTANCE_ID = st.secrets["INSTANCE_ID"]

from ai_prediction import predict_risk

import random

def collect_metrics():

    cpu = get_cpu_usage()

    memory = random.randint(40, 90)

    network = get_network_in()

    network_out = get_network_out()

    status_check = get_status_check()

    instance_state = get_instance_status(INSTANCE_ID)

    risk = predict_risk(cpu, memory, network)

    cpu_history = get_cpu_history()

    network_history = get_network_history()

    return {
        "cpu": cpu,
        "memory": memory,
        "network": network,
        "network_out": network_out,
        "status_check": status_check,
        "instance_state": instance_state,
        "risk": risk,
        "cpu_history": cpu_history,
        "network_history": network_history
    }