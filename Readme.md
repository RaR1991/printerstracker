# Printers Tracker

This project is a web interface built with Flask to display printer status information obtained from printers connected to the local network. It was a quick project developed for my role as an IT support for Asian Cup 2023 in order to make it easy to track printers in my venue. The printers were mainly Xerox MFP C315 and WorkCentre 7855.

## Features

- Display printer status including IP, serial number (SN), location, and toner levels.
- Displaying additional information such as replace needed.

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/RaR1991/printerstracker.git
   ```

2. Install the required dependencies:

   ```bash
   pip install -r requirements.txt
   ```

3. Run the Flask application:

   ```bash
   python app.py
   ```

4. Open your web browser and navigate to `http://localhost:5000` to view the printer status web interface.

## Other Scripts

In addition to the main Flask web interface, this project folder contains the following scripts:

- `set_location.py`: A script for setting the location of Xerox MFP C315 printers using data from a JSON file.
- `infos_via_snmp.py`: A script for collecting print counters from printers using SNMP.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
