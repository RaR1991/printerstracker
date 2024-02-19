from concurrent.futures import ThreadPoolExecutor, as_completed
import requests
from bs4 import BeautifulSoup
import re
from json import dumps, load


with open("printers_infos.json", "r") as locFile:
    known_locations = load(locFile)
    known_locations = known_locations["WC7855"]
    # print(known_locations)


wt_re = re.compile(r"Waste Toner Container\n\s+(\w+)")
ink_re = re.compile(r"(\w+\sToner)[\n\s]+(\w+)[\n\s]+(\d{1,3})")
ink_re = re.compile(r"(\w+\sToner)[\n\s]+(\w+)[\n\s]+(\d{1,3})[%\n\s]+(\d{1,5})")
a3_infos_re = re.compile(
    r"Name:[\s\n]+([\w ]+)[\w\W\s\n]+Machine Model:[\s\n]+([\w ]+)[\s\n]+Serial Number:[\s\n]+([\w ]+)[\s\n]+IPv4 Address:[\s\n]+(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})"
)
remove_spaces = lambda item: (
    item[0],
    item[1].replace(" v1 Multifunction System", ""),
    item[2],
    item[3],
    known_locations[item[3]]["location"],
)

headers = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
    "Accept-Language": "en-US;q=0.9",
    "Connection": "keep-alive",
    "Cookie": "PageToShow=; statusNumNodes=9; statusSelected=n6",
    "DNT": "1",
    "Upgrade-Insecure-Requests": "1",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
}


def get_printer_infos(ip=""):
    try:
        url = f"http://{ip}/stat/general.php"
        payload = ""
        global headers
        response = requests.request(
            "GET", url, data=payload, headers=headers, verify=False, timeout=10
        )
        # print(response.text)
        soup = BeautifulSoup(response.text, "html.parser").prettify()
        soup = BeautifulSoup(soup, "html.parser")
        btext = soup.body.text

        # print(a3_infos_re.findall(btext)[0])
        st = remove_spaces(a3_infos_re.findall(btext)[0])
        # print(st)
        pr_infos = {
            "IP": ip,
            "SN": st[2],
            "Location": st[4],
        }
        return pr_infos
    except Exception as e:
        print(e)
        return {
            "IP": ip,
            "SN": "Unknown",
            "Location": "Unknown",
        }


def ink_status(ip=""):
    try:
        url = f"http://{ip}/stat/consumables.php"
        payload = ""
        global headers
        response = requests.request(
            "GET", url, data=payload, headers=headers, verify=False, timeout=10
        )
        soup = BeautifulSoup(response.text, "html.parser").prettify()
        soup = BeautifulSoup(soup, "html.parser")
        btext = soup.body.text
        # print(btext)
        btext = re.sub(r"\xA0", " ", btext)
        status = ink_re.findall(btext)
        sup_info = {}
        for s in status:
            # print(s)
            sup_info[s[0]] = {"currentStatus": s[1], "currentlevel": s[2], "rp": s[3]}
        wc_status = wt_re.findall(btext)[-1]
        try:
            if wc_status:
                sup_info["Toner Bottle"] = {
                    "currentStatus": wc_status,
                    "currentlevel": 100,
                    "rp": 0,
                }
            else:
                sup_info["Toner Bottle"] = {
                    "currentStatus": "Unavailable",
                    "currentlevel": 100,
                    "rp": 0,
                }
        except Exception as e:
            sup_info["Toner Bottle"] = {
                "currentStatus": "Unavailable",
                "currentlevel": 100,
                "rp": 0,
            }
        # print(sup_info)
        return sup_info
    except Exception as e:
        return {
            "Black Toner": {"currentStatus": "Unknown", "currentlevel": 0, "rp": 0},
            "Cyan Toner": {"currentStatus": "Unknown", "currentlevel": 0, "rp": 0},
            "Magenta Toner": {"currentStatus": "Unknown", "currentlevel": 0, "rp": 0},
            "Toner Bottle": {"currentStatus": "Unknown", "currentlevel": 0, "rp": 0},
            "Yellow Toner": {"currentStatus": "Unknown", "currentlevel": 0, "rp": 0},
        }


def fetch_printer_info(ip):
    all_infos = get_printer_infos(ip)
    all_infos.update(ink_status(ip))
    return all_infos


def get_wc_printers():
    all_printers = []
    with ThreadPoolExecutor(max_workers=10) as executor:
        futures = {
            executor.submit(fetch_printer_info, ip): ip for ip in known_locations.keys()
        }
        for future in as_completed(futures):
            ip = futures[future]
            try:
                all_infos = future.result()
                all_printers.append(all_infos)
            except Exception as e:
                print(f"Failed to fetch information for printer {ip}: {e}")
    return sorted(all_printers, key=lambda x: x["IP"])


if __name__ == "__main__":
    print(ink_status("172.16.3.42"))
