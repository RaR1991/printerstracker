"""
Script to update the location information of printers connected to the network.
"""

import requests
from urllib.parse import quote
from json import load

# Load printer information from JSON file
with open("printers_infos.json", "r") as jf:
    printers = load(jf)["C315"]


def set_location(ip="", location=""):
    """
    Function to update the location information of a printer.

    :param ip: IP address of the printer.
    :param location: New location to set for the printer.
    """
    try:
        # Construct URL
        url = f"http://{ip}/webglue/content"

        # Encode location information
        qloc = quote('{"AboutPrinterLoc":"' + location + '"}')

        # Construct payload
        payload = f"data={qloc}&c=AboutThisPrinter&lang=fr"

        # Define headers
        headers = {
            "Accept": "application/json, text/javascript, */*; q=0.01",
            "Accept-Language": "en-US,en;q=0.9",
            "Connection": "keep-alive",
            "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
            "Cookie": "lang=fr",
            "DNT": "1",
            "Origin": f"http://{ip}/",
            "Referer": f"http://{ip}/",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "X-KL-saas-Ajax-Request": "Ajax_Request",
            "X-Requested-With": "XMLHttpRequest",
        }

        # Send POST request to update location
        response = requests.request("POST", url, data=payload, headers=headers)

        # Print response
        print(response.text)
    except Exception as e:
        # Handle exceptions
        print(f"{ip} {e}")


# Iterate over printers and update location
for ip in printers.keys():
    set_location(ip, printers[ip]["location"])
