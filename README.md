# 🌐 Automated Network Fault Detection System

A Docker-based system for simulating and detecting network anomalies using Linux Traffic Control and Machine Learning.

### 🏗 Architecture
1.  **Traffic-Generator**: Sends ICMP (Ping) requests to the Collector.
2.  **Gateway (DUT)**: Simulates network faults (latency, packet loss and corruption) using `tc` (Traffic Control).
3.  **Collector**: Captures raw network traffic data via Python `subprocess`.
4.  **Parser**: Processes raw collector logs into structured data.
5.  **ML**: Detects anomalies using the **Isolation Forest** algorithm.

### 🛠 Tech Stack
- **Infrasctructure**: Docker, Docker Compose
- **Networking**: Linux `tc` (netem), ICMP/Ping, `subprocess`
- **Analysis**: Python (Pandas, Scikit-Learn)
