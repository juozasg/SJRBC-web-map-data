import os
from datetime import datetime, timedelta
import requests

from api.common import Timeseries, TimeseriesRecord


# 392 - Baugo Creek CR 1
# 393 - NB1 - North Branch Elkhart River - Topeka (W800S)
# 394 - Phillips Ditch Station 2 (Kern Road)
# 395 - NB3 - North Branch Elkhart River - Milford (IN-3)

# 396 - Phillips Ditch Station 1 (U.S. 20)
# 397 - NB2 - North Branch Elkhart River - Kendallville (N600E)
# 398 - Fawn River (FR1) - Nevada Mills (N500W)
# 399 - Little Elkhart River at US-120 (7805)


# 399 is offline since feb 2026 but previous data is good
tolthawk_valid_sensors = [392, 393, 394, 395, 396, 397, 398, 399]

# sensor ID to polynomial params X^2, X, C
curves: dict[int, list[float]] = {
    392: [-1.26075370976264,    1_910.26485060629,      -723_129.95585746],
    393: [-32.3888163018327,    57_369.2128341629,      -25_403_968.3756699],
    394: [ 1.345813553894,      -2_133.975147433,       845_920.284518411],
    395: [ 7.76489716486637,    -14_639.4554711765,     6_900_080.39497958],
    396: [ 8.89159482087575,    -13_855.6495255451,     5_397_769.6745776],
    397: [ 23.1681316279053,    -43_368.9631642991,     20_295_836.7829409],
    398: [ 3.92295660400168,    -7_487.8476610553,      3_572_965.82237962],
    399: [ 43.313898878434,     -65_456.634484499,      24_729_779.9770313],
}

sealevels: dict[int, float] = {
    392: 738.16,
    393: 882.62,
    394: 794.87,
    395: 940.5,
    396: 778.38,
    397: 935.33,
    398: 956.65,
    399: 756.33
}


def height_to_streamflow(sensor_id, waterlevel):
    # return waterlevel * 10
    x2, x, c = curves[sensor_id]
    # print(x2, x, c, waterlevel)
    return (x2 * waterlevel * waterlevel) + (x * waterlevel) + c


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
    if debug:
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
    return api_readings_to_timeseries(response.json(), debug)

def api_readings_to_timeseries(readings: list[dict], debug = False) -> Timeseries:
    tseries: Timeseries = []
    for reading in readings:
        timestamp = int(datetime.fromisoformat(reading['DT']).timestamp())
        waterlevel = reading['WLV']
        # groundheight = reading['GH']
        sensor_id = reading['Lid']
        waterlevel = float(waterlevel) + sealevels[sensor_id]
        if waterlevel >= 0:
            flow = height_to_streamflow(sensor_id, waterlevel)
            if debug:
                print("READING", reading, 'SL waterlevel', waterlevel, 'flow', flow)
            tseries.append(TimeseriesRecord(timestamp=timestamp, flow=flow, height=float(waterlevel)))
    return tseries

if __name__ == "__main__":
    # print(get_region_status())
    # print(get_sensor_status(393))
    end_dt = datetime.now()
    # start_dt = end_dt - timedelta(hours=24)
    start_dt = end_dt - timedelta(days=10)

    fetch_tolthawk_iv(393, start_dt, end_dt, True)
    # fetch_tolthawk_iv(392, datetime(2026, 1, 16), datetime(2026, 1, 17), True)


