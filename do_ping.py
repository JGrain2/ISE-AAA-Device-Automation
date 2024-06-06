#do_ping.py - Ping a network device using Netmiko and Python

import subprocess
import config

# Get the IP address from the config.py file
ip = config.DEVICE_IP
def do_ping(ip):
    try:
        # Ping the IP address
        output = subprocess.run(["ping", "-c", "1", ip], capture_output=True, text=True)
        if output.returncode == 0:
            print(f"Ping to {ip} was successful.")
            print(output.stdout)
        else:
            print(f"Ping to {ip} failed.")
            print(output.stderr)
    except Exception as e:
        print(f"An error occurred: {e}")

# Call the function
if __name__ == "__main__":     
    do_ping(ip)