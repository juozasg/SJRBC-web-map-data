from datetime import datetime
import dateutil
import pytz

import requests

from .common import Timeseries, TimeseriesRecord

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
    elif 'Gage height' in name:
        return 'height'
    else:
        return None



def fetch_usgs_iv(sensor_id: str, from_dt: datetime, to_dt: datetime) -> Timeseries:
    start = from_dt.strftime('%Y-%m-%dT%H:%M:%SZ')
    end = to_dt.strftime('%Y-%m-%dT%H:%M:%SZ')

    url = f'https://waterservices.usgs.gov/nwis/iv/?format=json&sites={sensor_id}&siteStatus=all&startDT={start}&endDT={end}'
    print(f"Fetching usgs-{sensor_id} from {url}")

    response = requests.get(url)
    response.raise_for_status()

    # Parse response JSON
    return usgs_ts_to_timeseries(response.json()['value']['timeSeries'])

def usgs_ts_to_timeseries(series: list[dict]) -> Timeseries:
    tseries: Timeseries = []
    for s in series:
        variable_name = s['variable']['variableName']
        variable_type = varname(variable_name)
        if variable_type != 'flow':
            continue
        for value_entry in s['values'][0]['value']:
            date_time = dateutil.parser.isoparse(value_entry['dateTime']).astimezone(pytz.utc)
            value = float(value_entry['value'])
            tseries.append(TimeseriesRecord(timestamp=int(date_time.timestamp()), flow=value))

    return tseries

if __name__ == "__main__":
    print(fetch_usgs_iv('04096515', datetime(2024, 1, 1), datetime(2024, 1, 3)))
