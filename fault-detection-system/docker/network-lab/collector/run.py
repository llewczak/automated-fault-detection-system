import os
import subprocess
import time
from datetime import datetime

log_file = "/logs/collector_logs.txt"

if os.path.exists(log_file):
    os.remove(log_file)

with open(log_file, "w") as file:
        file.write("")

os.system("ip route add 172.21.0.0/24 via 172.22.0.10")

cmd = ["tcpdump", "-i", "any", "-n", "-l", "icmp"]

try:
    with subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True) as proc:
        with open(log_file, "a") as f:
            for line in proc.stdout:
                if "IP" in line:
                    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    clean_line = line.strip()
                    f.write(f'{timestamp},{clean_line}\n')
                    f.flush()
except KeyboardInterrupt:
    print("Stopping collector...")