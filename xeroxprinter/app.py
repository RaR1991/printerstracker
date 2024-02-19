from flask import Flask, render_template, jsonify, Response
import json
from c315_mt import get_all_printers
from printers_in_lan_mt import get_wc_printers
import pandas as pd
from datetime import datetime

app = Flask(__name__)

printer_data = []  # Initialize an empty list to store printer data


# Home route to render the HTML template
@app.route("/wc")
def wc():
    printer_data = get_wc_printers()
    # print(printer_data)
    try:
        return render_template("wc.html", printer_data=printer_data)
    except Exception as e:
        return render_template(
            "wc.html",
            printer_data=[
                {
                    "IP": "0.0.0.0",
                    "SN": "",
                    "Location": "Unknown",
                    "Black Toner": {
                        "currentStatus": "Unknown",
                        "currentlevel": 0,
                        "rp": 0,
                    },
                    "Cyan Toner": {
                        "currentStatus": "Unknown",
                        "currentlevel": 0,
                        "rp": 0,
                    },
                    "Magenta Toner": {
                        "currentStatus": "Unknown",
                        "currentlevel": 0,
                        "rp": 0,
                    },
                    "Toner Bottle": {
                        "currentStatus": "Unknown",
                        "currentlevel": 0,
                        "rp": 0,
                    },
                    "Yellow Toner": {
                        "currentStatus": "Unknown",
                        "currentlevel": 0,
                        "rp": 0,
                    },
                }
            ],
        )


# Home route to render the HTML template
@app.route("/")
def home():
    printer_data = get_all_printers()
    # print(printer_data)
    try:
        return render_template("index.html", printer_data=printer_data)
    except Exception as e:
        return render_template(
            "index.html",
            printer_data=[
                {
                    "IP": "0.0.0.0",
                    "SN": "",
                    "Location": "Unknown",
                    "Black Toner": {"currentStatus": "Unknown", "currentlevel": 0},
                    "Cyan Toner": {"currentStatus": "Unknown", "currentlevel": 0},
                    "Magenta Toner": {"currentStatus": "Unknown", "currentlevel": 0},
                    "Toner Bottle": {"currentStatus": "Unknown", "currentlevel": 0},
                    "Yellow Toner": {"currentStatus": "Unknown", "currentlevel": 0},
                }
            ],
        )


if __name__ == "__main__":
    app.run(debug=True)
