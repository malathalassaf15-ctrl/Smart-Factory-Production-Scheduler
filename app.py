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
                "Start_Hrs": start_hrs,
                "Finish_Hrs": finish_hrs,
                "Start": start_dt,
                "Finish": finish_dt,
                "Duration (hrs)": job["Duration (hrs)"],
                "Priority": job["Priority"],
            }
        )
        machine_available_time[earliest_machine_idx] = finish_hrs

    df = pd.DataFrame(schedule_data)
    makespan = max(machine_available_time)
    avg_utilization = (sum(df["Duration (hrs)"]) / (makespan * num_machines)) * 100
    bottleneck_machine = f"Machine {machine_available_time.index(makespan) + 1}"

    return df, makespan, avg_utilization, bottleneck_machine


jobs = generate_jobs(num_jobs)
df_schedule, makespan, avg_utilization, bottleneck_machine = run_schedule(
    jobs, num_machines, strategy
)

col1, col2, col3 = st.columns(3)
col1.metric("Total Production Time (Makespan)", f"{makespan} hrs")
col2.metric("Average Line Utilization", f"{avg_utilization:.1f}%")
col3.metric("Critical Bottleneck Station", bottleneck_machine)

st.markdown("---")

st.subheader("📊 Interactive Line Balancing & Schedule (Gantt Chart)")
fig = px.timeline(
    df_schedule,
    x_start="Start",
    x_end="Finish",
    y="Machine",
    color="Job",
    hover_data=["Priority", "Duration (hrs)", "Start_Hrs", "Finish_Hrs"],
    title="Optimized Job Sequence Across Factory Machines",
)
fig.update_yaxes(autorange="reversed")
fig.update_layout(
    xaxis_title="Production Timeline", yaxis_title="Work Center / Machine"
)
st.plotly_chart(fig, use_container_width=True)

st.subheader("📋 Scheduled Work Order Breakdown")
st.dataframe(
    df_schedule[
        ["Job", "Machine", "Start_Hrs", "Finish_Hrs", "Duration (hrs)", "Priority"]
    ],
    use_container_width=True,
)

st.markdown("---")

st.subheader("⚖️ Compare LPT vs SPT Heuristics")
st.write(
    "Runs both scheduling heuristics on the same set of jobs and machines, "
    "so you can see which one actually produces a shorter makespan."
)

if st.button("🔍 Run Heuristic Comparison"):
    comparison_jobs = generate_jobs(num_jobs)

    _, lpt_makespan, lpt_util, lpt_bottleneck = run_schedule(
        comparison_jobs, num_machines, "Longest Processing Time First (LPT)"
    )
    _, spt_makespan, spt_util, spt_bottleneck = run_schedule(
        comparison_jobs, num_machines, "Shortest Processing Time First (SPT)"
    )

    comparison_df = pd.DataFrame(
        [
            {
                "Heuristic": "LPT (Longest Processing Time First)",
                "Makespan (hrs)": lpt_makespan,
                "Avg Utilization (%)": round(lpt_util, 1),
                "Bottleneck Machine": lpt_bottleneck,
            },
            {
                "Heuristic": "SPT (Shortest Processing Time First)",
                "Makespan (hrs)": spt_makespan,
                "Avg Utilization (%)": round(spt_util, 1),
                "Bottleneck Machine": spt_bottleneck,
            },
        ]
    )

    st.dataframe(comparison_df, use_container_width=True)

    better = "LPT" if lpt_makespan <= spt_makespan else "SPT"
    diff = abs(lpt_makespan - spt_makespan)
    pct_diff = (diff / max(lpt_makespan, spt_makespan)) * 100

    st.success(
        f"✅ For this job set, **{better}** produced the shorter makespan — "
        f"{diff} hrs faster ({pct_diff:.1f}% improvement) than the other heuristic."
    )

    fig_compare = px.bar(
        comparison_df,
        x="Heuristic",
        y="Makespan (hrs)",
        color="Heuristic",
        title="Makespan Comparison: LPT vs SPT",
        text="Makespan (hrs)",
    )
    st.plotly_chart(fig_compare, use_container_width=True)
