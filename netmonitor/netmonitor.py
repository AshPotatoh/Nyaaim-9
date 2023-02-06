import time
import psutil
import requests

# Get initial network usage statistics

byte_list = []

time_counter = 0

while True:
    net_io_counters1 = psutil.net_io_counters()

    # Wait for some time
    time.sleep(1)

    # Get final network usage statistics
    net_io_counters2 = psutil.net_io_counters()

    # Calculate the difference in bytes sent
    bytes_sent = net_io_counters2.bytes_sent - net_io_counters1.bytes_sent

    # Calculate the difference in bytes received
    bytes_recv = net_io_counters2.bytes_recv - net_io_counters1.bytes_recv
    if bytes_recv < 3500 and len(byte_list) < 1200:
        byte_list.append(bytes_recv)
        time_counter += 1
        print(len(byte_list))
	
    elif len(byte_list) >= 1200:
        byte_list = []
        body = {"action": "shutdown", "api_key": "<yourAPIKey>"}
        r = requests.post("http://<yourIP>/api/v1/dcs_shutdown", json=body)
        #reply = r.json()
        print(r)
    elif time_counter >= 1360 and len(byte_list) < 1200:
        byte_list = []
        time_counter = 0
    else:
        continue
        


    print(bytes_recv)