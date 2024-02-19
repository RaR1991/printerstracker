"""
Script to retrieve printer information using SNMP and store it in an Excel file.
"""

from pysnmp.hlapi import *
from json import load
import pylightxl as xl
from time import sleep


# Function to perform an SNMP walk on a device
def snmpwalk(host, community, oids, loc_eng):
    """
    Function to perform an SNMP walk on a device.

    :param host: IP address of the device.
    :param community: SNMP community string.
    :param oids: List of OIDs to query.
    :param loc_eng: SNMP engine.
    :return: List of results from SNMP walk.
    """
    results = []

    for oid in oids:
        iterator = getCmd(
            loc_eng,
            CommunityData(community),
            UdpTransportTarget((host, 161)),
            ContextData(),
            ObjectType(ObjectIdentity(oid)),
            lexicographicMode=False,
        )

        for errorIndication, errorStatus, errorIndex, varBinds in iterator:
            if errorIndication:
                print(f"Error: {errorIndication}")
                break
            elif errorStatus:
                print(f"Error: {errorStatus.prettyPrint()}")
                break
            else:
                for varBind in varBinds:
                    queried_oid, value = varBind
                    results.append(value.prettyPrint())
    return results


# SNMP server details
host = "172.16.3.74"
community = "public"
oids = [
    "1.3.6.1.2.1.43.5.1.1.17.1",  # OID for the printer's SN
    "1.3.6.1.4.1.253.8.53.13.2.1.6.1.20.101",  # Total number of black impressions
    "1.3.6.1.4.1.253.8.53.13.2.1.6.1.20.102",  # Total number of color impressions
    "1.3.6.1.4.1.253.8.53.13.2.1.6.1.20.44",  # Total number of black large impressions
    "1.3.6.1.4.1.253.8.53.13.2.1.6.1.20.43",  # Total number of color large impressions
    "1.3.6.1.4.1.253.8.53.13.2.1.6.1.20.1",  # Total number of all impressions
]

# Load printer information from JSON file
with open("printers_infos.json", "r") as pf:
    pcount = []
    loc_eng = SnmpEngine()
    data = load(pf)["WC7855"]
    for key in data.keys():
        print(key)
        r = snmpwalk(key, community, oids, loc_eng)
        r = [key, data[key]["location"]] + r
        pcount.append(r)
    db = xl.Database()

    # add a blank worksheet to the db
    db.add_ws(ws="WC7855_Counters")

    # loop to add data to the worksheet
    for col_id, data in enumerate(pcount, start=1):
        print(data)
        for row_id, data in enumerate(data, start=1):
            db.ws(ws="WC7855_Counters").update_index(row=col_id, col=row_id, val=data)

    # write out the db
    xl.writexl(db=db, fn="printer_counts.xlsx")
