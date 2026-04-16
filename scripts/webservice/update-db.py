# cache USGS NWIS daily data in CSV format under datasets

import csv
import os
from datetime import datetime, timezone

import pytz

from api.common import Timeseries
from api.tolthawk import fetch_tolthawk_iv, tolthawk_valid_sensors
from api.usgs import fetch_usgs_iv, usgs_ids


def append_csv(path, timeseries: Timeseries):
    with open(path, 'a', newline='') as csvfile:
        csv_writer = csv.writer(csvfile)
        # csv_writer.writerow(['ts', 'flow'])
        for record in timeseries:
            csv_writer.writerow([record.timestamp, record.flow])
    print(f'appended {len(timeseries)} records to {path}')


def last_datetime(csv_file):
    lines = 0
    with open(csv_file) as f:
        for line in f:
            lines += 1
            pass
    last_line = line
    if lines == 1:
        return datetime(2026, 4, 1, 0, 0, tzinfo=pytz.utc)

    ts = last_line.split(',')[0]
    try:
        dt = datetime.fromtimestamp(float(ts) + 60, pytz.utc) # skip a minute to avoid duplicate records
        # print('last line for', csv_file, ts, dt)
        return dt
    finally:
        return datetime(2026, 4, 1, 0, 0, tzinfo=pytz.utc)


file_dir = os.path.dirname(__file__)

os.makedirs(file_dir + '/realtime-db', exist_ok=True)


# delta_dt = datetime(2025, 7, 1, 0, 0, tzinfo=pytz.utc)
now_dt = datetime.now(timezone.utc)



for site_id in usgs_ids:
    path = f'{file_dir}/realtime-db/usgs-{site_id}.csv'
    dt = last_datetime(path)

    append_ts: Timeseries = fetch_usgs_iv(site_id, dt, now_dt)
    append_csv(path, append_ts)

tt_ids = tolthawk_valid_sensors
for site_id in tt_ids:
    path = f'{file_dir}/realtime-db/tolthawk-{site_id}.csv'
    dt = last_datetime(path)

    append_ts: Timeseries = fetch_tolthawk_iv(site_id, dt, now_dt)

    append_csv(f'{file_dir}/realtime-db/tolthawk-{site_id}.csv', append_ts)




