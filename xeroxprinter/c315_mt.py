import concurrent.futures
import requests
from json import loads, load, dumps

known_locations = {}
with open("printers_infos.json", "r") as locFile:
    known_locations = load(locFile)
    known_locations = known_locations["C315"]

payload = ""
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:121.0) Gecko/20100101 Firefox/121.0",
    "Accept": "application/json, text/javascript, */*; q=0.01",
    "Accept-Language": "en-US,en;q=0.5",
    "Accept-Encoding": "gzip, deflate",
    "Content-Type": "application/x-www-form-urlencoded; charset=utf-8",
    "X-Requested-With": "XMLHttpRequest",
    "X-KL-saas-Ajax-Request": "Ajax_Request",
    "DNT": "1",
    "Connection": "keep-alive",
}


def c315_infos(ip=""):
    current_printer = {"IP": ip}
    global headers
    global payload
    global known_locations
    url = f"http://{ip}/webglue/rawcontent"

    querystring = {"timedRefresh": "1", "c": "Status"}
    try:
        response = requests.request(
            "GET",
            url,
            data=payload,
            headers=headers,
            params=querystring,
            verify=False,
            timeout=10,
        )

        printer_infos = loads(response.text)
        suplies = printer_infos["nodes"]["supplies"]
        printer_sn = printer_infos["nodes"]["nodes"]["DeviceSerialNumberUnq"]["text"][
            "text"
        ]
        current_printer["SN"] = printer_sn
        try:
            current_printer["Location"] = known_locations[ip]["location"]
        except Exception as e:
            current_printer["Location"] = "Unknown"

        for key in suplies.keys():
            if "Toner" in key:
                current_toner = suplies[key]
                current_printer[key] = {
                    "currentStatus": current_toner["currentStatus"],
                    "currentlevel": current_toner["curlevel"],
                }
        return current_printer
    except Exception as e:
        return {
            "IP": ip,
            "SN": "",
            "Location": "Unknown",
            "Black Toner": {"currentStatus": "Unknown", "currentlevel": 0},
            "Cyan Toner": {"currentStatus": "Unknown", "currentlevel": 0},
            "Magenta Toner": {"currentStatus": "Unknown", "currentlevel": 0},
            "Toner Bottle": {"currentStatus": "Unknown", "currentlevel": 0},
            "Yellow Toner": {"currentStatus": "Unknown", "currentlevel": 0},
        }


def get_all_printers():
    c315_ips = known_locations.keys()
    # c315_ips = [
    #     "172.16.3.66",
    #     "172.16.3.61",
    #     "172.16.3.28",
    #     "172.16.3.63",
    #     "172.16.3.39",
    #     "172.16.3.29",
    #     "172.16.3.30",
    #     "172.16.3.31",
    #     "172.16.3.73",
    #     "172.16.3.40",
    #     "172.16.3.22",
    #     "172.16.3.26",
    #     "172.16.3.69",
    #     "172.16.3.21",
    #     "172.16.3.68",
    #     "172.16.3.25",
    #     "172.16.3.37",
    #     "172.16.3.27",
    #     "172.16.3.23",
    #     "172.16.3.67",
    #     "172.16.3.32",
    #     "172.16.3.24",
    #     "172.16.3.38",
    #     "172.16.3.72",
    #     "172.16.3.75",
    # ]

    status_all = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
        futures = [executor.submit(c315_infos, ip) for ip in c315_ips]

        for future in concurrent.futures.as_completed(futures):
            try:
                status_all.append(future.result())
            except Exception as e:
                p = {
                    "IP": "Error",
                    "SN": e,
                    "Location": "Unknown",
                    "Black Toner": {"currentStatus": "Unknown", "currentlevel": 0},
                    "Cyan Toner": {"currentStatus": "Unknown", "currentlevel": 0},
                    "Magenta Toner": {"currentStatus": "Unknown", "currentlevel": 0},
                    "Toner Bottle": {"currentStatus": "Unknown", "currentlevel": 0},
                    "Yellow Toner": {"currentStatus": "Unknown", "currentlevel": 0},
                }
                status_all.append(p)

    return sorted(status_all, key=lambda x: x["IP"])


if __name__ == "__main__":
    print(get_all_printers())
