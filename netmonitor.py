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
    if bytes_recv < 2000 and len(byte_list) < 1200:
        byte_list.append(bytes_recv)
        time_counter += 1
    elif len(byte_list) >= 1200:
        byte_list = []
        headers = {"action": "shutdown"}
        r = requests.post("http://45.63.7.109:8000/api/v1/dcs_shutdown")
    elif time_counter >= 1200 and len(byte_list) < 1200:
        byte_list = []
        
        


    print(bytes_recv)