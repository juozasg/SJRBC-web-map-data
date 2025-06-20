# cache USGS NWIS daily data in CSV format under datasets

from datetime import datetime
import requests
import json
import csv
import os


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
endDate = '2011-05-01'  # For testing, use a fixed date

ids = ['04096405','04096515','04097500','040975299','04097540','04099000','04100500','04101000','04101500','04101800','04102500','04099750']
ids = ','.join(ids)
ids = '04101500'

url = f'https://waterservices.usgs.gov/nwis/dv/?format=json&sites={ids}&statCd=00003&siteStatus=all&startDT=2011-04-01&endDT={endDate}'
print(f"URL: {url}")

# Create datasets directory if it doesn't exist
os.makedirs('datasets', exist_ok=True)

# Get JSON data from URL
print(f"Fetching data from {url}")
response = requests.get(url)
if response.status_code == 200:
    data = response.json()

    # Open CSV file for writing
    with open('datasets/usgs.csv', 'w', newline='') as csvfile:
        csv_writer = csv.writer(csvfile)

        # Write header
        csv_writer.writerow(['siteId', 'date', 'flow', 'temp', 'spc', 'do'])


        # Extract timeSeries data
        for series in data['value']['timeSeries']:
            site_id = series['sourceInfo']['siteCode'][0]['value']
            site_id = 'usgs-' + site_id  # Prefix site ID with 'usgs'
            variable_name = series['variable']['variableName']
            variable_name = varname(variable_name)
            if variable_name is None:
                continue


            # Extract values
            for value_entry in series['values'][0]['value']:
                date_time = value_entry['dateTime']
                # split YYYY-MM-DDThh:mm:ss into date and time
                date_time = date_time.split('T')[0]
                value = value_entry['value']
                print(f"{site_id}: {variable_name} {date_time} {value}")

                # Write row to CSV

    print(f"Data saved to datasets/usgs.csv")
else:
    print(f"Failed to fetch data: {response.status_code}")

