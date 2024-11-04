import requests
from bs4 import BeautifulSoup
import re
import os
import ipaddress

# URL of the updated Microsoft's IPs list
url = 'https://networksdb.io/ip-addresses-of/microsoft-corp'

# GET request to the webpage
response = requests.get(url)

# Check if the request was successful
if response.status_code == 200:
    # Parse the HTML content
    soup = BeautifulSoup(response.content, 'html.parser')

    # Find all text in the soup that matches CIDR notation
    cidr_pattern = r'\b(?:\d{1,3}\.){3}\d{1,3}/\d{1,2}\b'
    cidrs = re.findall(cidr_pattern, soup.get_text())

    # Define the path for saving the IP addresses
    ip_directory_path = os.path.join(os.path.expanduser('~'), 'C:\\Users\\user\\MicrosoftIPTXT', 'Microsoft_IP_Addresses.txt')

    # Create the directory if it doesn't exist
    os.makedirs(os.path.dirname(ip_directory_path), exist_ok=True)

    # Write the IP addresses to a text file
    with open(ip_directory_path, 'w') as f:
        for cidr in set(cidrs):  # Use set to avoid duplicates
            # Convert CIDR to IP addresses
            network = ipaddress.ip_network(cidr, strict=False)
            for ip in network.hosts():  # Get all usable host IPs
                f.write(str(ip) + '\n')

    print(f'Found {len(set(cidrs))} unique CIDRs and saved their IP addresses to {ip_directory_path}')
else:
    print(f'Failed to retrieve the webpage. Status code: {response.status_code}')