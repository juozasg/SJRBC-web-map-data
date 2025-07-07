import os
from datetime import datetime
import requests

from api.common import Timeseries, TimeseriesRecord

tolthawk_valid_sensors = [393, 394, 395, 396, 397, 398, 399]

# sensor ID to polynomial params X^2, X, C
curves: dict[int: [float, float, float]] = {
    393: [-33.4039,  59_168.1049,  -26_200_918.3488],
    394: [ 1.3458,  -2_133.9751,   845_920.2845],
    395: [ 7.9020,  -14_898.2806,  7_022_211.9933],
    396: [ 8.8916,  -13,855.6495,  5_397_769.6746],
    397: [ 40.5930, -76_601.0360,  36_137_494.6487],
    398: [-14.8347,  28_530.5057, -13_717_545.2763],
    399: [ 38.4723, -58_123.5123,  21_953_055.762],
}



def height_to_streamflow(sensor_id, waterlevel):
    return waterlevel * 10
    # x2, x, c = curves[sensor_id]
    # return (x2 * waterlevel * waterlevel) + (x * waterlevel) + c


def read_token():
    file_dir = os.path.dirname(__file__)
    with open(file_dir + '/tolthawk-token', 'r') as f:
        token = f.read().strip()
        return token


def get_region_status():
    region_id = 49
    url = f"https://sensors.tolthawk.com/api/mobile/LocationsStatus/{region_id}"

    headers = {
        "Content-Type": "application/json",
        "Token": read_token()
    }

    print(f"Fetching from {url}")
    response = requests.get(url, headers=headers)
    response.raise_for_status()

    # Parse response JSON
    data = response.json()
    # print(f"Successfully fetched data for {len(data)} sensors")
    # print(data)
    return data

def get_sensor_status(sensor_id: int):
    region_id = 49
    url = f"https://sensors.tolthawk.com/api/mobile/LocationsStatus/{region_id}/{sensor_id}"

    headers = {
        "Content-Type": "application/json",
        "Token": read_token()
    }

    print(f"Fetching tolthawk-{sensor_id} from {url}")
    response = requests.get(url, headers=headers)
    response.raise_for_status()

    # Parse response JSON
    data = response.json()
    # print(f"Successfully fetched data for {len(data)} sensors")
    # print(data)
    return data


def fetch_tolthawk_iv(sensor_id: int, from_dt: datetime, to_dt: datetime, debug = False) -> Timeseries:

    start = from_dt.strftime('%Y%m%d%H%M')
    end = to_dt.strftime('%Y%m%d%H%M')
    date_range = f"{start}-{end}2359"

    # sensor_id = 393
    url = f"https://sensors.tolthawk.com/api/mobile/WaterLevels/{sensor_id}/{date_range}"
    print(f"Fetching tolthawk-{sensor_id} from {url}")

    headers = {
        "Content-Type": "application/json",
        "Token": read_token()
    }

    response = requests.get(url, headers=headers)
    response.raise_for_status()

    if debug:
        print(response.json())
    # Parse response JSON
    return api_readings_to_timeseries(response.json())

def api_readings_to_timeseries(readings: list[dict]) -> Timeseries:
    tseries: Timeseries = []
    for reading in readings:
        # print("READING", reading)
        timestamp = int(datetime.fromisoformat(reading['DT']).timestamp())
        waterlevel = reading['WLV']
        groundheight = reading['GH']
        sensor_id = reading['Lid']
        flow = height_to_streamflow(sensor_id, waterlevel)
        tseries.append(TimeseriesRecord(timestamp=timestamp, flow=flow, height=float(waterlevel)))
    return tseries

if __name__ == "__main__":
    # print(get_region_status())
    # print(get_sensor_status(393))
    fetch_tolthawk_iv(395, datetime(2025, 7, 7), datetime(2025, 7, 8), True)


