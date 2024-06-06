#ise_autoadd.py - Auto-add a network device to Cisco ISE using Netmiko and Python

import requests
import json
from requests.auth import HTTPBasicAuth
import config

# Disable warnings for unverified HTTPS requests (not recommended for production)
requests.packages.urllib3.disable_warnings(requests.packages.urllib3.exceptions.InsecureRequestWarning)

# Use the variables from the config.py file
def add_device_to_ise(device_ip, device_name):
# Use the variables from the config.py file
    ISE_SERVER = config.ISE_SERVER
    USERNAME = config.USERNAME
    PASSWORD = config.PASSWORD
    DEVICE_IP = device_ip
    DEVICE_IP_MASK = config.DEVICE_IP_MASK
    RADIUS_KEY = config.RADIUS_KEY
    DEVICE_NAME = config.DEVICE_NAME
    DESCRIPTION = config.DESCRIPTION

    # API endpoints
    url = f"{ISE_SERVER}/ers/config/networkdevice"
    get_devices_url = f"{ISE_SERVER}/ers/config/networkdevice/name/{DEVICE_NAME}"

    # Headers for the request
    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json'
    }

    # Payload for the request
    payload = {
        'NetworkDevice': {
            'name': DEVICE_NAME,
            'description': DESCRIPTION,
            'NetworkDeviceIPList': [{
                'ipaddress': DEVICE_IP,
                'mask': DEVICE_IP_MASK
            }],
            'authenticationSettings': {
                'radiusSharedSecret': RADIUS_KEY
            }
        }
    }

    # Convert payload to JSON string
    payload_json = json.dumps(payload)

##############################################################################
    # Check if the device already exists
    try:
        # Check if the device already exists
        print(f"Checking if device {DEVICE_NAME} exists in Cisco ISE...")
        get_response = requests.get(
            get_devices_url,
            headers=headers,
            auth=HTTPBasicAuth(USERNAME, PASSWORD),
            verify=False  # Set to True if you have proper SSL certificates
        )
#        print(get_response.text)

        # If the device exists, print a message and exit the script
        if get_response.status_code == 200:
            print(f"This device, {DEVICE_NAME}, already exists.")
        elif get_response.status_code == 404:
            print(f"Device {DEVICE_NAME} does not exist. Proceeding to add the device...")

            # Send POST request to add the network device
            response = requests.post(
                url,
                headers=headers,
                data=payload_json,
                auth=HTTPBasicAuth(USERNAME, PASSWORD),
                verify=False  # Set to True if you have proper SSL certificates
            )

            # Check for success
            if response.status_code == 201:
                print(f"Successfully added device {DEVICE_IP} to Cisco ISE.")
            else:
                print(f"Failed to add device. Status code: {response.status_code}, Response: {response.text}")
        else:
            print(f"Unexpected response when checking for device existence. Status code: {get_response.status_code}, Response: {get_response.text}")
#        print(get_response.text)

    except requests.exceptions.ConnectionError as ce:
        print(f"Connection error occurred: {ce}")
    except requests.exceptions.HTTPError as he:
        print(f"HTTP error occurred: {he}")
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")