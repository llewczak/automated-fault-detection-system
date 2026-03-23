import time
import os
import random
from datetime import datetime
import numpy as np

def get_datetime():
	timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
	return timestamp

def generate_packets(t):
      base_number_of_packets = np.random.normal(12.5,1.2)
      drift = 2 * np.sin(t/100)
      result = int(base_number_of_packets + drift)
      return max(0, result)

destination_ip = "172.22.0.20"

print("Generator starting...")

time.sleep(5)

print("Setting up routes...")

while True:
    status = os.system("ip route add 172.22.0.0/24 via 172.21.0.10")
    if status == 0:
        print("Network route configured successfully!")
        break
    else:
        print("Waiting for Gateway (172.21.0.10) to be reachable...")
        time.sleep(2)

log_file = "/logs/generator_logs.txt"
if os.path.exists(log_file):
    os.remove(log_file)

with open(log_file, "w") as file:
	file.write("date,destination_ip,number_of_tickets\n")

os.system("ip route del default")
os.system("ip route add default via 172.21.0.10")

i = 0

with open(log_file, 'a', encoding='utf-8') as file:
	while True:
		number_of_packets = generate_packets(i)
		os.system(f'ping -c {number_of_packets} -i 0.2 {destination_ip}') 
		file.write(f'{get_datetime()},{destination_ip},{number_of_packets}\n')
		file.flush()
		i += 1
		time.sleep(0.25)
