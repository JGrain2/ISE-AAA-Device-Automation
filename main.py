# main.py - Auto-add multiple network devices to Cisco ISE using Netmiko and Python

import os
import netmiko
from netmiko import ConnectHandler
import do_ping
import ise_autoadd
import config
import get_hostname
import importlib

# Ping the device / Hostname / Commands
def process_device(device_ip):
    try:
        print(f'Pinging {device_ip}...')
        do_ping.do_ping(device_ip)
    except Exception as e:
        print(f"An error occurred while pinging {device_ip}: {e}")
        return

    try:
        print(f'Checking the hostname for {device_ip}...')
        get_hostname.set_hostname(device_ip)
        # Reload the config module
        importlib.reload(config)
        print(f'Hostname for {device_ip} is {config.DEVICE_NAME}')
        
    except Exception as e:
        print(f"An error occurred while getting the hostname for {device_ip}: {e}")
        return

    # Open the 'commands.ios' file and read its contents
    with open('commands.ios') as f:
        commands_list = f.read().splitlines()
        
    # Establish SSH connection
    cisco = {
        'device_type': 'cisco_ios',
        'ip': device_ip,
        'username': config.DEVICE_USERNAME,
        'password': config.DEVICE_PASSWORD,
        'secret': config.DEVICE_SECRET,
    }

    # Connect to the device
    try:
        print(f'Connecting to device: {device_ip}...')
        net_connect = ConnectHandler(**cisco)
        print(f"Connected to {device_ip}.")

        # Enter enable mode
        net_connect.enable()
        print("Entered enable mode.")

        # Send configuration commands
        print("Sending configuration commands...")
        output = net_connect.send_config_set(commands_list)
        print("Commands sent.")
        print(output)

        # Close the connection
        net_connect.disconnect()
        print("Disconnected from device.")

        # Add device to Cisco ISE
        print(f'Adding deivce: {device_ip} to Cisco ISE...')
        ise_autoadd.add_device_to_ise(device_ip, config.DEVICE_NAME)
        print(f'Device {device_ip} had been added to Cisco ISE.') 
        
    except netmiko.NetmikoTimeoutException:
        print("Connection timed out.")
    except netmiko.NetmikoAuthenticationException:
        print("Authentication failed.")
    except Exception as e:
        print(f"An error occurred with device {device_ip}: {e}")

# Main
if __name__ == "__main__":
    print(f"Current working directory: {os.getcwd()}")

    # List all files in the current directory
    #print("Files in the current directory:")
    #for filename in os.listdir(os.getcwd()):
    #    print(f" - {filename}")
    
    # Check if 'device_ips.txt' exists
    device_ips_path = os.path.join(os.getcwd(), 'device_ips.txt')
    print(f'Using device_ips.txt path: {device_ips_path}')
    
    # Read device IPs from file
    try:
        with open(device_ips_path) as file:
            device_ips = file.read().splitlines()
    except FileNotFoundError:
        print("device_ips.txt file not found.")
        exit(1)
    # Process each device IP
    for device_ip in device_ips:
        print(f"\nProcessing device with IP: {device_ip}")
        process_device(device_ip)