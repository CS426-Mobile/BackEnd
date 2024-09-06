import os
import subprocess
import re

def get_ip():
    # Run the ipconfig command and get the output
    result = subprocess.run(['ipconfig'], capture_output=True, text=True)
    
    # Extract all sections of the ipconfig output
    sections = result.stdout.split("\n\n")
    
    # Initialize variable to store the IP address
    ip_address = None

    # Loop through each section to find an active network adapter with a valid IPv4 address
    is_next = False
    for section in sections:
        # Look for IPv4 Address lines, ignoring "Media disconnected"
        if "Wireless LAN adapter Wi-Fi:" in section:
            is_next = True
            continue
        if is_next and 'IPv4 Address' in section:
            # Extract the IPv4 address from the section
            ip_match = re.search(r"IPv4 Address[^\d]*([\d\.]+)", section)
            if ip_match:
                ip_address = ip_match.group(1)
                break  # Use the first valid IP address found
    
    if ip_address:
        return ip_address
    else:
        return "No IPv4 address found."

def run_django_server():
    # Get the current directory
    script_directory = os.path.dirname(os.path.abspath(__file__))  # This gets the directory where the script is stored
    
    # Get the user's IP address
    ip_address = get_ip()
    
    if not ip_address:
        print("No IPv4 address found.")
        return
    
    print(f"Starting Django server at http://{ip_address}:8000/")
    
    # Command to start the Django server
    command = f'py manage.py runserver {ip_address}:8000'
    
    # Open command prompt, move to current directory, and run the command
    subprocess.run(['cmd', '/c', f'cd /d {script_directory} && {command}'])

# Run the Django server with your IP
run_django_server()
