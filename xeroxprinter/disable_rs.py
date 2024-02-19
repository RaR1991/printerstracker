import requests
from json import load


with open("printers_infos.json", "r") as jf:
    printers = load(jf)


print(printers["C315"].keys())


def disable_rs(ip=""):
    try:
        url = f"http://{ip}/webglue/content"

        payload = "data=%7B%22XeroxDataUploadContent-XRS_PushEnabled%22%3A%220%22%7D&c=XeroxDataUpload&lang=en"
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:121.0) Gecko/20100101 Firefox/121.0",
            "Accept": "application/json, text/javascript, */*; q=0.01",
            "Accept-Language": "en-US,en;q=0.5",
            "Accept-Encoding": "gzip, deflate",
            "Content-Type": "application/x-www-form-urlencoded; charset=utf-8",
            "X-Requested-With": "XMLHttpRequest",
            "X-KL-saas-Ajax-Request": "Ajax_Request",
            "Origin": f"http://{ip}",
            "DNT": "1",
            "Connection": "keep-alive",
            "Referer": f"http://{ip}/",
            "Cookie": "lang=en",
        }

        response = requests.request(
            "POST", url, data=payload, headers=headers, timeout=10
        )

        print(response.text)
    except Exception as e:
        print(f"{ip} {e}")


for ip in printers["C315"].keys():
    disable_rs(ip)
