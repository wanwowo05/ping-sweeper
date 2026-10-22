import subprocess
import concurrent.futures
from datetime import datetime

def ping_host(ip):
    """Pings an IP address silently and returns it if active."""
    # Windows ping command: -n 1 (send 1 packet), -w 500 (wait 500ms)
    command = ['ping', '-n', '1', '-w', '500', ip]
    
    # Run the command silently in the background
    result = subprocess.run(command, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    
    # Return code 0 means the ping was successful
    if result.returncode == 0:
        return ip
    return None

network_prefix = input("Enter the network prefix to sweep (e.g., 192.168.0): ")

print("-" * 100)
print(f"Sweeping network: {network_prefix}.X")
print(f"Time started: {datetime.now()}")
print("-" * 100)

active_hosts = []

# Use 50 "workers" to check 50 IP addresses at the exact same time
with concurrent.futures.ThreadPoolExecutor(max_workers=50) as executor:
    # Create a list of IPs from .1 to .254
    ips_to_scan = [f"{network_prefix}.{i}" for i in range(1, 255)]
    
    # Run the ping_host function on all IPs simultaneously
    results = executor.map(ping_host, ips_to_scan)
    
    for result in results:
        if result:
            print(f"[+] Host {result} is ACTIVE")
            active_hosts.append(result)

print("-" * 50)
print(f"Sweep completed! Found {len(active_hosts)} active hosts.")