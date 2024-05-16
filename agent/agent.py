import os
import requests
from scapy.all import *

def post_score_token():
    # Define the IP address of the server
    ip = os.environ.get('SCORE_SERVER_IP')
    # Define the port number of the server
    port = int(os.environ.get('SCORE_SERVER_PORT'))
    # Define the score token
    score_token = os.environ.get('SCORE_TOKEN')
    exercise_id = os.environ.get('EXERCISE_ID')

    response = requests.post(f'http://{ip}:{port}/exercises/{exercise_id}/submit',
                  json={'answer': score_token})
    print(response.json())


def handle_icmp(packet):
    if packet.haslayer(ICMP):
        print("Received ICMP request from", packet[IP].src)
        post_score_token()

print("Sniffing ICMP packets...")
# Sniff ICMP packets
sniff(filter="icmp", prn=handle_icmp)