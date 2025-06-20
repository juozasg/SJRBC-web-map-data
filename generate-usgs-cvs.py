# cache USGS NWIS daily data in CSV format under datasets

from datetime import datetime
import requests
import json
import csv
import os
from collections import defaultdict
# import local python file
import dates_with_records as dwr


def varname(variable_name):
    # find substring in variable_name and return a more readable name
    if 'Temperature' in variable_name:
        return 'temp'
    elif 'Streamflow' in variable_name:
        return 'flow'
    elif 'Specific conductance' in variable_name:
        return 'spc'
    elif 'Dissolved oxygen' in variable_name:
        return 'do'
    else:
        return None


endDate = datetime.now().strftime('%Y-%m-%d')
# endDate = '2011-05-01'  # For testing, use a fixed date

ids = ['04096405','04096515','04097500','040975299','04097540','04099000','04100500','04101000','04101500','04101800','04102500','04099750']
ids = ','.join(ids)
# ids = '04101500'  # For testing with a single site

url = f'https://waterservices.usgs.gov/nwis/dv/?format=json&sites={ids}&statCd=00003&siteStatus=all&startDT=1981-01-01&endDT={endDate}'
print(f"URL: {url}")

# Create datasets directory if it doesn't exist
os.makedirs('datasets', exist_ok=True)

# Get JSON data from URL
print(f"Fetching data from {url}")
response = requests.get(url)
if response.status_code == 200:
    data = response.json()

    # Create a nested dictionary to store data by site_id and date
    # Structure: site_data[site_id][date] = {'flow': value, 'temp': value, etc.}
    site_data = defaultdict(lambda: defaultdict(dict))

    # Extract timeSeries data
    for series in data['value']['timeSeries']:
        site_id = series['sourceInfo']['siteCode'][0]['value']
        site_id = 'usgs-' + site_id  # Prefix site ID with 'usgs'

        variable_name = series['variable']['variableName']
        variable_type = varname(variable_name)

        if variable_type is None:
            continue

        # Extract values
        for value_entry in series['values'][0]['value']:
            date_time = value_entry['dateTime'].split('T')[0]  # Get just the date part
            value = value_entry['value']

            # Store the value in our nested dictionary
            site_data[site_id][date_time][variable_type] = value
            print(f"Collected: {site_id}: {variable_type} {date_time} {value}")


    # sort each site_id's dates
    for site_id in site_data:
        site_data[site_id] = dict(sorted(site_data[site_id].items()))

    unique_dates = dwr.get_unique_dates()
    # delete dates that do not have records
    for site_id in list(site_data.keys()):
        for date in list(site_data[site_id].keys()):
            if date not in unique_dates:
                del site_data[site_id][date]
    # Open CSV file for writing
    with open('datasets/usgs.csv', 'w', newline='') as csvfile:
        csv_writer = csv.writer(csvfile)

        # Write header
        csv_writer.writerow(['siteId', 'date', 'flow', 'temp', 'spc', 'do'])

        # Write data rows
        for site_id, dates in site_data.items():
            for date, variables in dates.items():
                row = [
                    site_id,
                    date,
                    variables.get('flow', ''),  # Use empty string if variable doesn't exist
                    variables.get('temp', ''),
                    variables.get('spc', ''),
                    variables.get('do', '')
                ]
                csv_writer.writerow(row)

    print(f"Data saved to datasets/usgs.csv")
else:
    print(f"Failed to fetch data: {response.status_code}")

