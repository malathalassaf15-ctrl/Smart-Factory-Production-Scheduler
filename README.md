# 🏭 Smart Factory Production Scheduler & Line Balancer

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://smart-factory-appuction-scheduler-9vzdws353jmswitecpuf3w.streamlit.app/#interactive-line-balancing-and-schedule-gantt-chart)

An automated heuristic scheduling engine built in Python to optimize job sequencing, balance machine loads, and minimize total production completion time (**Makespan**) in high-mix manufacturing environments.

🚀 **[Click here to launch the Live Interactive Dashboard](https://smart-factory-appuction-scheduler-9vzdws353jmswitecpuf3w.streamlit.app/#interactive-line-balancing-and-schedule-gantt-chart)**

---

## 🎯 The Problem
In modern manufacturing, inefficient job sequencing leads to:
* **High Machine & Labor Idle Time:** Unbalanced work centers leave expensive equipment sitting idle.
* **Production Bottlenecks:** Poorly planned job queues create severe operational bottlenecks.
* **Unpredictable Deliveries:** Unoptimized order sequences lead to missed customer deadlines.

Calculating the absolute optimal schedule across multiple machines is an $NP\text{-hard}$ optimization problem. This tool uses dynamic heuristic dispatching rules (**Longest Processing Time / Shortest Processing Time**) to sequence jobs and balance workloads in real time.

---

## ✨ Key Features & Capabilities
* **Dynamic Load Balancing:** Automatically assigns incoming work orders to the earliest available machine to equalize capacity.
* **Interactive Gantt Charts:** Generates real-time, interactive production schedules built with `Plotly`.
* **Bottleneck Detection:** Instantly flags critical path machines and calculates total line utilization metrics.
* **Real-Time Scenario Testing:** Allows operational managers to adjust machine counts and job volumes on the fly via a **Streamlit** cloud dashboard.

---

## 🛠️ Tech Stack
* **Language:** Python
* **Data Processing:** Pandas
* **Data Visualization:** Plotly
* **Web App Deployment:** Streamlit

---
---
## 🚀 How to Run Locally
1. Clone the repository:
```bash
   git clone https://github.com/malathalassaf15-ctrl/Smart-Factory-Production-Scheduler.git
```
2. Navigate into the project folder:
```bash
   cd Smart-Factory-Production-Scheduler
```
3. Install dependencies:
```bash
   pip install -r requirements.txt
```
4. Launch the dashboard:
```bash
   streamlit run app.py
```
---
## ⚖️ Heuristic Comparison Mode
Beyond running a single scheduling strategy, the dashboard includes a **Compare LPT vs SPT Heuristics** tool. It runs both dispatching rules on the identical set of jobs and machines, then reports which heuristic actually produces the shorter makespan — turning an abstract scheduling choice into a concrete, measurable result.

## 📊 Live Web Application
You can test different production parameters, switch dispatching rules, and analyze machine utilization live here:
👉 **[Launch Smart Factory App](https://smart-factory-appuction-scheduler-9vzdws353jmswitecpuf3w.streamlit.app/#interactive-line-balancing-and-schedule-gantt-chart)**
