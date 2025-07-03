from datetime import datetime

import requests

from scripts.api.common import Timeseries, TimeseriesRecord


ids = [397, 395, 398, 396, 394, 392, 399]


def height_to_streamflow(sensor_id, waterlevel):
    return waterlevel * 11.0


def read_token():
    with open('tolthawk-token', 'r') as f:
        token = f.read().strip()
        return token


# def get_sensor_status(region_id):
#     url = f"https://sensors.tolthawk.com/api/mobile/LocationsStatus/{region_id}"
#
#     response = requests.get(url, headers=headers)
#     response.raise_for_status()
#
#     # Parse response JSON
#     data = response.json()
#     print(f"Successfully fetched data for {len(data)} sensors")
#     print(data)
#     return data


def fetch_tolthawk_iv(sensor_id: int, from_dt: datetime, to_dt: datetime) -> Timeseries:
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

    # Parse response JSON
    return api_readings_to_timeseries(response.json())

def api_readings_to_timeseries(readings: list[dict]) -> Timeseries:
    tseries: Timeseries = []
    for reading in readings:
        timestamp = int(datetime.fromisoformat(reading['DT']).timestamp())
        waterlevel = reading['WLV']
        sensor_id = reading['Lid']
        flow = height_to_streamflow(sensor_id, waterlevel)
        tseries.append(TimeseriesRecord(timestamp=timestamp, flow=flow))
    return tseries

if __name__ == "__main__":
    print(fetch_tolthawk_iv(392, datetime(2024, 1, 1), datetime(2024, 1, 3)))