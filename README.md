# Smart-Factory-Production-Scheduler
# 🏭 Smart Factory Production Scheduler & Line Balancer

An automated heuristic scheduling engine built in Python to optimize job sequencing, balance machine loads, and minimize total production completion time (**Makespan**) in high-mix manufacturing environments.

---

## 🎯 The Problem
In modern manufacturing, inefficient job sequencing leads to:
* High worker and machine idle time.
* Severe equipment bottlenecks.
* Unpredictable order completion times and missed delivery deadlines.

Calculating the absolute optimal schedule across multiple machines is a complex optimization problem ($NP\text{-hard}$). This tool uses heuristic decision rules (**Longest Processing Time First / Shortest Processing Time First**) to assign jobs to machines in seconds, balancing line load dynamically.

---

## ✨ Key Features
* **Dynamic Load-Balancing Engine:** Automatically assigns incoming work orders to the earliest available machine.
* **Interactive Gantt Chart Visualization:** Generates real-time, color-coded timelines built with `Plotly`.
* **Bottleneck Identification:** Instantly flags the critical path machine and overall line utilization metrics.
* **Scenario Testing:** Allows operational managers to test different dispatching rules and machine capacities on the fly via a **Streamlit** cloud app.

---

## 🛠️ Tech Stack
* **Language:** Python
* **Data Processing:** Pandas
* **Visualization:** Plotly
* **Web Framework:** Streamlit
