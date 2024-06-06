import netmiko
import config

def set_hostname(device_ip):
    device = {
        'device_type': 'cisco_ios',
        'ip': device_ip,
        'username': config.DEVICE_USERNAME,
        'password': config.DEVICE_PASSWORD,
        'secret': config.DEVICE_SECRET,
        'timeout': 60,
        'conn_timeout': 60
    }

    try:
        # Establish SSH connection to the device
        print("Connecting to device to set hostname...")
        net_connect = netmiko.ConnectHandler(**device)
        print(f"Connected to {device['ip']}.")
        
        # Enter enable mode
        if 'secret' in device:
            net_connect.enable()
            print("Entered enable mode.")

        # Set hostname
        output = net_connect.send_command('show run | include hostname')
        print(output)
        print(f'Output from show run command: {output}')
        hostname = output.split()[1]
        if not hostname:
            raise ValueError('Hostname not found in output')
        print(f'Current hostname: {hostname}')

        # Update hostname in config.py   
        update_device_name_in_config(hostname)

        # Close the connection
        net_connect.disconnect()
        print("Disconnected from device.")

    except netmiko.NetmikoTimeoutException:
        print("Connection timed out.")
    except netmiko.NetmikoAuthenticationException:
        print("Authentication failed.")
    except Exception as e:
        print(f"An error occurred: {e}")
        
# Update DEVICE_NAME in config.py
def update_device_name_in_config(hostname):
    """
    Updates the value of the `DEVICE_NAME` variable in the `config.py` file with the given `hostname`.
    
    Parameters:
        hostname (str): The new value for the `DEVICE_NAME` variable.
    
    Returns:
        None
    
    Raises:
        Exception: If an error occurs while updating the `DEVICE_NAME` variable in the `config.py` file.
    """
    try:
        print(f"Updating DEVICE_NAME in config.py to {hostname}...")
        with open('config.py', 'r') as f:
            lines = f.readlines()
            
        with open('config.py', 'w') as f:
            for line in lines:
                if line.startswith('DEVICE_NAME ='):
                    print(f'Replacing {line.strip()} with DEVICE_NAME = \"{hostname}\"')
                    line = f'DEVICE_NAME = "{hostname}"\n'
                f.write(line)
        print(f"Updated DEVICE_NAME in config.py to {hostname}.")
    except FileNotFoundError:
        print("config.py file not found. Unable to update DEVICE_NAME.")
    except Exception as e:
        print(f"An error occurred while updating DEVICE_NAME in config.py: {e}")

# Call the function
if __name__ == "__main__":
    set_hostname()