import time
import os
import random
from datetime import datetime, timedelta 

def apply_tc(command):
	os.system("tc qdisc del dev eth1 root 2>/dev/null")
	os.system(f'tc qdisc add dev eth1 root {command}')

def get_time_window(seconds=10):
    now = datetime.now()
    end_time = now + timedelta(seconds=seconds)
    
    start_str = now.strftime("%Y-%m-%d %H:%M:%S")
    end_str = end_time.strftime("%Y-%m-%d %H:%M:%S")
    return start_str, end_str

os.system("sysctl -w net.ipv4.ip_forward=1")
os.system("iptables -F")
os.system("iptables -A FORWARD -j ACCEPT")
os.system("iptables -t nat -A POSTROUTING -o eth0 -j MASQUERADE")
os.system("iptables -t nat -A POSTROUTING -o eth1 -j MASQUERADE")

print("Gateway started...")

log_file = "../logs/gateway_logs.txt"
if os.path.exists(log_file):
    os.remove(log_file)

with open(log_file, "w") as file:
        file.write("start_date,end_date,action\n")


with open(log_file, "a") as file:
	while True:
		probability = random.randint(1,100)
		start_date, end_date = get_time_window()
		if probability <= 5:
			probability = random.randint(0,2)
			if probability < 1:
				apply_tc("netem delay 100ms")
				file.write(f'{start_date},{end_date},DELAY\n')
			elif probability < 2:
				apply_tc("netem loss 25%")
				file.write(f'{start_date},{end_date},LOSS\n')
			else:
				apply_tc("netem corrupt 10%")
				file.write(f'{start_date},{end_date},CORRUPTION\n')
		else:
			os.system("tc qdisc del dev eth1 root 2>/dev/null")
			file.write(f'{start_date},{end_date},NORMAL\n')
		file.flush()
		time.sleep(10)
