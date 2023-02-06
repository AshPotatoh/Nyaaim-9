import os
import time
import requests
import json
from os import getenv

token = os.getenv("VULTR_TOKEN")


def dcs_server_stop():
    
    headers = {"Authorization": "Bearer "+ token}
    r = requests.get("https://api.vultr.com/v2/instances", headers=headers)
    reply = r.json()
    print(str(reply) + "\n\n------------------\n\n")
    for instances in reply['instances']:
        print("this ran")
        print(instances['label'])
        if instances['label'] == "dcs-server":
            print("this ran 2")
            instance_id = instances['id']
            print("this ran 3")
            print(instance_id + "\n\n------------------\n\n" + instances['hostname'])
            print("this ran 4")
            snapshot_body = {"description": "dcs-server", "instance_id": instance_id}
            snapshot_post = requests.post('https://api.vultr.com/v2/snapshots', headers=headers, json=snapshot_body)
            print(snapshot_post.text)
            time.sleep(10)  
    snapshot_api_status = True
    while snapshot_api_status == True:
        snapshot_status = requests.get("https://api.vultr.com/v2/instances", headers=headers)
        snapshot_reply = snapshot_status.json()
        for instances in snapshot_reply['instances']:
            if instances['label'] == "dcs-server":
                instance_id = instances['id']
                if instances['server_status'] == "ok":
                    print("active")
                    snapshot_api_status = False
                    
                else:
                    print("not active")
                    time.sleep(1)
        
    print(instance_id)
    shutdown = requests.delete("https://api.vultr.com/v2/instances/"+instance_id, headers=headers)
    print(shutdown.text)
    return "Server is shutting down! :slight_frown: You can start the server by using \n ```!dcs start```"
    

def dcs_server_status():

    headers = {"Authorization": "Bearer " + token}
    r = requests.get("https://api.vultr.com/v2/instances", headers=headers)

    reply = r.json()

    
    
    for host in reply['instances']:
        instance= host['id']
        status = host['status']
        main_ip = host['main_ip']
        hostname = host['hostname']
        if status == "active" and hostname == "dcs-server":
            online_list = [instance, status, main_ip]
            print(online_list)
            return "The server is online! :smile: \n Status: " + online_list[1] + "\n Main IP: " + online_list[2] +":10308", True
            

        else:
            continue
    return "The server is offline! :slight_frown: You can start the server by using \n ```!dcs start```", False
    
    


def dcs_server_start():
    headers = {"Authorization": "Bearer "+ token}
    
    #need to remove this id, and have it get this on its own.
    block_get = requests.get("https://api.vultr.com/v2/blocks", headers=headers)
    block_reply = block_get.json()
    print(block_reply)
    dcs_block = ""
    for block in block_reply['blocks']:
        if block['label'] == "dcs-storage":
            dcs_block = block['id']
            print(dcs_block)
            break
        else:
            continue
    
    snapshot = requests.get("https://api.vultr.com/v2/snapshots", headers=headers)
    snapshot_reply = snapshot.json()
    print(snapshot_reply)
    latest_snapshot = snapshot_reply["snapshots"][-1]['id']
    
    #getting the ip address
    r_ips = requests.get("https://api.vultr.com/v2/reserved-ips", headers=headers)
    reply_ips = r_ips.json()
    for ip in reply_ips['reserved_ips']:
        if ip['label'] == "dcs-reserved-ip":
            reserved_ip = ip['id']
            ipaddr = ip['subnet']
            print(reserved_ip, " ", ipaddr)

    instance_body = {"region": "ewr", "plan": "vc2-4c-8gb", "label": "dcs-server", "snapshot_id": latest_snapshot, "reserved_ipv4": reserved_ip, "hostname": "dcs-server"}
    snapshot_id = latest_snapshot
    print(snapshot_id)
    restore = requests.post("https://api.vultr.com/v2/instances", headers=headers, json=instance_body)
    print("\nrestore: " + str(restore.text))
    restore_reply = restore.json()
    print(restore_reply)
    restore_instance = restore_reply["instance"]
    instance_id = restore_instance["id"]
    print(instance_id + "<---- instance id for new server")
    start_up = True
    time.sleep(35)
    while start_up == True:
        r = requests.get("https://api.vultr.com/v2/instances", headers=headers)
        reply = r.json()
        for host in reply['instances']:
            if host["id"] == instance_id:
                if host['server_status'] == "ok":
                    print("active")
                    start_up = False
                    break
                else:
                    print("not active")
                    time.sleep(1)
    block_body = {"instance_id": instance_id, "live": False}
    attach_block = requests.post("https://api.vultr.com/v2/blocks/"+ dcs_block +"/attach", headers=headers, json=block_body)
    #block_reply = attach_block.json()
    r_final = requests.get("https://api.vultr.com/v2/instances", headers=headers)
    reply_final = r_final.json()
    for host in reply_final['instances']:
        if host['hostname'] == "dcs-server":
            instance_id = host['id']
    

    
    print(block_reply)

    return "Server is up and running! :D You can connect to the server with the following IP: " + ipaddr


     


