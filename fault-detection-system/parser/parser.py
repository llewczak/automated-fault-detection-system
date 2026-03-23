from datetime import datetime
import os
import shutil
import re
import pandas as pd

private_key_path = "C:/Users/User/Desktop/AGH/projekt_qa/ssh-key-2026-03-19.key"
user_name = "ubuntu"
server_ip = "158.180.37.183"
path_to_files = "/home/ubuntu/network-lab/logs"

def get_data():
    if os.path.isdir("./logs"):
        shutil.rmtree("./logs")
    os.system(f"scp -i {private_key_path} -r {user_name}@{server_ip}:{path_to_files} ./")


def preprocess_collector_data(data):
    pattern = re.compile(
        r"((?P<date>\d{4}-\d{2}-\d{2})\s+\d{2}:\d{2}:\d{2},)?"
        r"(?P<timestamp>\d{2}:\d{2}:\d{2}\.\d+)\s+"
        r"(?P<iface>\w+)\s+"
        r"(?P<direction>In|Out)\s+"
        r"IP\s+(?P<source>[\d.]+)\s+>\s+(?P<destination>[\d.]+):\s+"
        r"ICMP echo (?P<type>request|reply), id (?P<id>\d+), seq (?P<seq>\d+), length (?P<length>\d+)"
    )
    parsed_data = []
    last_pending_request = None
    is_request_pending = False
    last_id = None
    last_seq = None
    last_in_timestamp = None
    current_active_date = None
    lines = [line.strip() for line in data.split("\n") if "ICMP" in line]

    for line in lines:
        match = pattern.search(line)
        if not match:
            continue

        d = match.groupdict()

        if d['date']:
            current_active_date = d['date']

        current_id = int(d['id'])
        current_seq = int(d['seq'])
        current_timestamp = datetime.strptime(d['timestamp'], "%H:%M:%S.%f")

        if d['type'] == 'request':
            if is_request_pending:
                parsed_data.append(last_pending_request)

            iat = (current_timestamp - last_in_timestamp).total_seconds() if last_in_timestamp else 0.0
            session_start = 0
            seq_diff = 1
            if last_id is not None:
                if current_id != last_id:
                    session_start = 1
                else:
                    seq_diff = current_seq - last_seq
            last_pending_request = {
                'date': current_active_date,
                'timestamp': d['timestamp'],
                'id': current_id,
                'seq': current_seq,
                'rtt': None,
                'iat': iat,
                'length': int(d['length']),
                'seq_difference': seq_diff,
                'session_start': session_start,
                'has_reply': 0
            }
            last_in_timestamp = current_timestamp
            last_id = current_id
            last_seq = current_seq
            is_request_pending = True
        elif d['type'] == 'reply':
            if is_request_pending and last_pending_request['id'] == current_id and last_pending_request['seq'] == current_seq:
                request_timestamp = datetime.strptime(last_pending_request['timestamp'], "%H:%M:%S.%f")
                rtt = (current_timestamp - request_timestamp).total_seconds()
                last_pending_request['rtt'] = rtt
                last_pending_request['has_reply'] = 1
                parsed_data.append(last_pending_request)
                is_request_pending = False

    if is_request_pending:
        parsed_data.append(last_pending_request)

    return parsed_data

def parse_data():
    get_data()
    with open('./logs/collector_logs.txt', 'r') as file:
        raw_log = file.read()
    data = preprocess_collector_data(raw_log)
    df = pd.DataFrame(data, columns=['date', 'timestamp', 'id', 'seq', 'rtt', 'iat', 'length', 'seq_difference',
                                     'session_start', 'has_reply'])
    df.to_csv("./parsed_csv/data.csv", index=False)

parse_data()