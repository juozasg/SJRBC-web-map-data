# cache USGS NWIS daily data in CSV format under datasets

from datetime import datetime

import pytz

import dateutil
import requests
import json
import csv
import os
from collections import defaultdict
# import local python file
import dates_with_records as dwr


def varname(name: str):
    # find substring in variable_name and return a more readable name
    if 'Temperature' in name:
        return 'temp'
    elif 'Streamflow' in name:
        return 'flow'
    elif 'Specific conductance' in name:
        return 'spc'
    elif 'Dissolved oxygen' in name:
        return 'do'
    else:
        return None


startDate = '2023-03-01'
endDate = datetime.now().strftime('%Y-%m-%d')
# endDate = '2023-03-02'

# endDate = '2011-05-01'  # For testing, use a fixed date

ids = ['04096405','04096515','04097500','040975299','04097540','04099000','04100500','04101000','04101500','04101800','04102500','04099750']
ids = ','.join(ids)
# ids = '04101500'  # For testing with a single site

url = f'https://waterservices.usgs.gov/nwis/iv/?format=json&sites={ids}&siteStatus=all&startDT={startDate}&endDT={endDate}'
print(f"URL: {url}")

# Create datasets directory if it doesn't exist
os.makedirs('15min', exist_ok=True)

# Get JSON data from URL
print(f"Fetching data from {url}")
response = requests.get(url)
if response.status_code == 200:
    data = response.json()

    # Create a nested dictionary to store data by site_id and date
    # Structure: site_data[site_id][date] = {'flow': value, 'temp': value, etc.}
    site_data: dict[str, dict[datetime, dict[str, float]]] = dict()

    # Extract timeSeries data
    for series in data['value']['timeSeries']:
        site_id = series['sourceInfo']['siteCode'][0]['value']
        site_id: str = 'usgs-' + site_id  # Prefix site ID with 'usgs'

        if not (site_id in site_data):
            site_data[site_id] = dict()

        variable_name = series['variable']['variableName']
        variable_type = varname(variable_name)

        if variable_type is None:
            continue

        # Extract values
        for value_entry in series['values'][0]['value']:
            date_time = dateutil.parser.isoparse(value_entry['dateTime']).astimezone(pytz.utc)
            value = float(value_entry['value'])

            # Store the value in our nested dictionary
            if not (date_time in site_data[site_id]):
                site_data[site_id][date_time] = dict()

            site_data[site_id][date_time][variable_type] = value
            # print(f"Collected: {site_id}: {variable_type} {date_time} {value}")


    # sort each site_id's dates
    for site_id in site_data:
        site_data[site_id] = dict(sorted(site_data[site_id].items()))


    # Open CSV file for writing
    with open('15min/usgs.csv', 'w', newline='') as csvfile:
        csv_writer = csv.writer(csvfile)

        # Write header
        csv_writer.writerow(['siteId', 'date', 'flow'])

        # Write data rows
        for site_id, dates in site_data.items():
            for date, variables in dates.items():
                row = [
                    site_id,
                    date.strftime("%Y-%m-%dT%H:%M:%SZ"),
                    variables.get('flow', ''),  # Use empty string if variable doesn't exist
                ]
                csv_writer.writerow(row)

    print(f"Data saved to 15min/usgs.csv")
else:
    print(f"Failed to fetch data: {response.status_code}")

