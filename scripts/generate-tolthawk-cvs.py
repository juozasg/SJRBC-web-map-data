import requests
from datetime import datetime
import csv


# Region ID for sensors
regionId = 49
startDate = '20220718'
endDate = datetime.now().strftime('%Y%m%d')
# endDate = '20220722'
dateRange = f"{startDate}0000-{endDate}2359"


def height_to_streamflow(date, height):
    # Convert water height to streamflow (cufs) using a simple linear model
    # This is a placeholder function; replace with actual conversion logic
    return height * 10  # Example conversion factor


def read_token():
    with open('tolthawk-token', 'r') as f:
        token = f.read().strip()
        return token

headers = {
    "Content-Type": "application/json",
    "Token": read_token()
}



def get_sensor_status(region_id):
    url = f"https://sensors.tolthawk.com/api/mobile/LocationsStatus/{region_id}"

    response = requests.get(url, headers=headers)
    response.raise_for_status()

    # Parse response JSON
    data = response.json()
    print(f"Successfully fetched data for {len(data)} sensors")
    return data

def get_water_levels(sensor_id):
    url = f"https://sensors.tolthawk.com/api/mobile/WaterLevels/{sensor_id}/{dateRange}"
    print(f"Fetching tolthawk-{sensor_id} from {url}")

    response = requests.get(url, headers=headers)
    response.raise_for_status()

    # Parse response JSON
    data = response.json()
    print(f"Successfully fetched readings for sensor {sensor_id}")
    return data

# Main execution
# TODO: collect all readings for each day and write mean water level to tolthawk.csv

sensor_status = get_sensor_status(regionId)
sites: dict[int, dict] = dict()

for sensor in sensor_status:
    sensor_id = sensor['Lid']
    created_on = sensor['CreatedOn']
    # print(sensor_id, sen)
    # print(sensor)
    # print(f"Sensor ID: {sensor_id}")
    readings = get_water_levels(sensor_id)

    # datetime list of reeadings or average reading per dat
    sites[sensor_id]: dict[str, list[float] | float] = dict()
    for reading in readings:
        date_time = reading['DT'].split('T')[0]
        waterlevel = reading['WLV']
        flow = height_to_streamflow(date_time, waterlevel)

        if date_time not in sites[sensor_id]:
            sites[sensor_id][date_time] = []

        sites[sensor_id][date_time].append(flow)


    # Calculate mean flow for each date
    for date, flows in sites[sensor_id].items():
        mean_flow = sum(flows) / len(flows)
        sites[sensor_id][date] = mean_flow

    print(len(readings), "readings", len(sites[sensor_id]), "days", "| mean flow", sum(sites[sensor_id].values()) / (len(sites[sensor_id]) or 1))
    # sort dates
    sites[sensor_id] = dict(sorted(sites[sensor_id].items()))

with open('../datasets/tolthawk.csv', 'w', newline='') as csvfile:
    csv_writer = csv.writer(csvfile)

    # Write header
    csv_writer.writerow(['siteId', 'date', 'flow'])
    # Write data rows
    for sensor_id, dates in sites.items():
        for date, flow in dates.items():
            csv_writer.writerow([f'tolthawk-{sensor_id}', date, flow])

    print(f"Data written to datasets/tolthawk.csv for {len(sites)} sensors")



    # print(sites)
    # print("total days:", len(sites[sensor_id]))
    # exit(0)


    # print(sensor_status)
    # sensor_id = 1001  # Example sensor ID, replace with actual ID

