import requests
from datetime import datetime

# Region ID for sensors
regionId = 49
startDate = '20150101'
startDate = '20250620'
endDate = datetime.now().strftime('%Y%m%d')
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
print(sensor_status)
exit(0)
for sensor in sensor_status:
    print(sensor)
    # sensor_id = sensor['Lid']
    # print(f"Sensor ID: {sensor_id}")
    readings = get_water_levels(sensor_id)
    print(f"Water levels for {sensor_id}:")
    for reading in readings:
        datetime = reading['DT']
        waterlevel = reading['WLV']
        print(reading)
        exit(0)


    # print(sensor_status)
    # sensor_id = 1001  # Example sensor ID, replace with actual ID

