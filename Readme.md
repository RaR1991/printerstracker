Printer Status Web Interface

This project is a web interface built with Flask to display printer status information obtained from printers connected to the local network. It was a quick project developed for my role as an IT support for Asian Cup 2023 in order to make it easy to track printers in my venue. The printers were mainly Xerox MFP C315 and WorkCentre 7855.
Features

    Display printer status including IP, serial number (SN), location, and toner levels.
    Automatically refreshes printer status every 10 minutes using AJAX.
    Bootstrap styling for a pleasant user interface.
    Supports displaying additional information such as replace status (rp).

Installation

    Clone the repository:

    bash

git clone https://github.com/your-username/printer-status.git

Install the required dependencies:

bash

pip install -r requirements.txt

Run the Flask application:

bash

    python app.py

    Open your web browser and navigate to http://localhost:5000 to view the printer status web interface.

Usage

    The printer status table displays information about printers connected to the local network.
    The table automatically refreshes every 10 minutes to display the latest printer status.
    Printer status is color-coded for easy identification: green for OK, orange for low toner, and red for replace status.

Author

    Rabah Ait Ramdane

License

This project is licensed under the MIT License - see the LICENSE file for details.