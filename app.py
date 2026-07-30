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

# Mock Job Generation Engine
import random

random.seed(42)
jobs = [
    {
        "Job ID": f"Order-{i+1:02d}",
        "Duration (hrs)": random.randint(2, 12),
        "Priority": random.choice(["High", "Medium", "Standard"]),
    }
    for i in range(num_jobs)
]

# Sorting strategy for scheduling
if strategy == "Longest Processing Time First (LPT)":
    sorted_jobs = sorted(
        jobs, key=lambda x: x["Duration (hrs)"], reverse=True
    )
else:
    sorted_jobs = sorted(jobs, key=lambda x: x["Duration (hrs)"])

# Scheduling Engine Logic (Greedy Heuristic Load-Balancing)
machine_available_time = [0] * num_machines
schedule_data = []

for job in sorted_jobs:
    # Find the machine that finishes earliest
    earliest_machine_idx = machine_available_time.index(
        min(machine_available_time)
    )
    start_time = machine_available_time[earliest_machine_idx]
    finish_time = start_time + job["Duration (hrs)"]

    schedule_data.append(
        {
            "Machine": f"Machine {earliest_machine_idx + 1}",
            "Job": job["Job ID"],
            "Start": start_time,
            "Finish": finish_time,
            "Duration": job["Duration (hrs)"],
            "Priority": job["Priority"],
        }
    )

    machine_available_time[earliest_machine_idx] = finish_time

df_schedule = pd.DataFrame(schedule_data)

# Key Performance Indicators (KPIs)
makespan = max(machine_available_time)
avg_utilization = (
    sum(df_schedule["Duration"]) / (makespan * num_machines)
) * 100
bottleneck_machine = f"Machine {machine_available_time.index(makespan) + 1}"

col1, col2, col3 = st.columns(3)
col1.metric("Total Production Time (Makespan)", f"{makespan} hrs")
col2.metric("Average Line Utilization", f"{avg_utilization:.1f}%")
col3.metric("Critical Bottleneck Station", bottleneck_machine)

st.markdown("---")

# Interactive Gantt Chart
st.subheader("📊 Interactive Line Balancing & Schedule (Gantt Chart)")
fig = px.timeline(
    df_schedule,
    x_start="Start",
    x_end="Finish",
    y="Machine",
    color="Job",
    hover_data=["Priority", "Duration"],
    title="Optimized Job Sequence Across Factory Machines",
)
fig.update_yaxes(autorange="reversed")
fig.update_layout(
    xaxis_title="Timeline (Hours)", yaxis_title="Work Center / Machine"
)
st.plotly_chart(fig, use_container_width=True)

# Machine Load Breakdown Table
st.subheader("📋 Scheduled Work Order Breakdown")
st.dataframe(df_schedule[["Job", "Machine", "Start", "Finish", "Duration", "Priority"]], use_container_width=True)
