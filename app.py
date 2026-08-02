import random
import pandas as pd
import plotly.express as px
import streamlit as st

# Streamlit Layout Configuration
st.set_page_config(
    page_title="Smart Factory Production Scheduler", layout="wide"
)
st.title("🏭 Smart Factory Production Scheduler & Line Balancer")
st.write(
    "Automated heuristic scheduling engine to optimize job sequencing, minimize total production time (Makespan), "
    "and identify machine bottlenecks in real time."
)

# Sidebar - Operational Parameters
st.sidebar.header("⚙️ Factory Parameters")
num_machines = st.sidebar.slider("Available Machines", 2, 8, 4)
num_jobs = st.sidebar.slider("Pending Production Orders", 5, 25, 12)
strategy = st.sidebar.selectbox(
    "Scheduling Heuristic",
    [
        "Longest Processing Time First (LPT)",
        "Shortest Processing Time First (SPT)",
    ],
)


# Shared job generation, so every run (and both heuristics) use the same job set
def generate_jobs(num_jobs, seed=42):
    random.seed(seed)
    return [
        {
            "Job ID": f"Order-{i+1:02d}",
            "Duration (hrs)": random.randint(2, 12),
            "Priority": random.choice(["High", "Medium", "Standard"]),
        }
        for i in range(num_jobs)
    ]


# Shared scheduling engine, so both heuristics run through identical logic
def run_schedule(jobs, num_machines, strategy_name):
    if strategy_name == "Longest Processing Time First (LPT)":
        sorted_jobs = sorted(jobs, key=lambda x: x["Duration (hrs)"], reverse=True)
    else:
        sorted_jobs = sorted(jobs, key=lambda x: x["Duration (hrs)"])

    machine_available_time = [0] * num_machines
    schedule_data = []
    base_time = pd.Timestamp("2026-01-01 08:00:00")

    for job in sorted_jobs:
        earliest_machine_idx = machine_available_time.index(min(machine_available_time))
        start_hrs = machine_available_time[earliest_machine_idx]
        finish_hrs = start_hrs + job["Duration (hrs)"]
        start_dt = base_time + pd.Timedelta(hours=start_hrs)
        finish_dt = base_time + pd.Timedelta(hours=finish_hrs)

        schedule_data.append(
            {
                "Machine": f"Machine {earliest_machine_idx + 1}",
                "Job": job["Job ID"],
