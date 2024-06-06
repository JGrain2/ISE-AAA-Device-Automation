# Auto-Add Network Devices to Cisco ISE

Welcome to the Auto-Add Network Devices to Cisco ISE project! This set of Python scripts helps automate the process of adding network devices to Cisco Identity Services Engine (ISE) using Netmiko for SSH connections and various Python libraries for configuration management and API interactions.

## Table of Contents

- [Overview](#overview)
- [Prerequisites](#prerequisites)
- [Project Structure](#project-structure)
- [Troubleshooting](#troubleshooting)
- [Contributing](#contributing)

## Overview

This project aims to streamline the process of managing network devices by automating tasks such as:
1. Pinging devices to verify their availability.
2. Retrieving and updating device hostnames.
3. Sending configuration commands to devices.
4. Adding devices to Cisco ISE via API.

## Prerequisites

Before you get started, make sure you have the following:
- Python 3.x installed
- [Netmiko](https://github.com/ktbyers/netmiko) library
- Requests library
- Access to Cisco ISE with API enabled


## Project Structure
```
ISE-AAA-Device-Automation/
│
├── main.py                 # Main script to orchestrate the automation process
├── config.py               # Configuration file with device and ISE details
├── do_ping.py              # Script to ping network devices
├── get_hostname.py         # Script to retrieve and set device hostnames
├── ise_autoadd.py          # Script to add devices to Cisco ISE
├── commands.ios            # File with configuration commands to be sent to devices
├── device_ips.txt          # File with the list of device IP addresses
└── requirements.txt        # File listing the required Python packages
```



# Troubleshooting

## Common Issues
  1.	File Not Found: Ensure all files are in the same directory and paths are correct.
	2.	Authentication Errors: Verify the credentials in config.py.
	3.	Connection Timeouts: Check network connectivity and device accessibility.
	4.	API Errors: Ensure Cisco ISE API is accessible and credentials have the necessary permissions.

Debugging
	•	Add print statements or use a debugger to trace issues.
	•	Check network connectivity using ping or telnet commands.

# Contributing
We welcome contributions! Please fork the repository and create a pull request with your changes. 
