# cache USGS NWIS daily data in CSV format under datasets

import csv
import os
from datetime import datetime, timezone

import pytz

from api.common import Timeseries
from api.tolthawk import fetch_tolthawk_iv, tolthawk_valid_sensors
from api.usgs import fetch_usgs_iv, usgs_ids


def write_csv(path, timeseries: Timeseries):
    with open(path, 'w', newline='') as csvfile:
        csv_writer = csv.writer(csvfile)
        csv_writer.writerow(['ts', 'flow'])
        for record in timeseries:
            csv_writer.writerow([record.timestamp, record.flow])
    print(f'Wrote {len(timeseries)} records to {path}')

# import local python file
os.makedirs('../realtime/base', exist_ok=True)
os.makedirs('../realtime/delta', exist_ok=True)


start_dt =  datetime(2023, 3, 1, 0, 0, tzinfo=pytz.utc)
delta_dt = datetime(2025, 7, 1, 0, 0, tzinfo=pytz.utc)
now_dt = datetime.now(timezone.utc)

for site_id in usgs_ids:
    base_ts: Timeseries = fetch_usgs_iv(site_id, start_dt, delta_dt)
    delta_ts: Timeseries = fetch_usgs_iv(site_id, delta_dt, now_dt)

    write_csv(f'../realtime/base/usgs-{site_id}.csv', base_ts)
    write_csv(f'../realtime/delta/usgs-{site_id}.csv', delta_ts)

for site_id in tolthawk_valid_sensors:
    base_ts: Timeseries = fetch_tolthawk_iv(site_id, start_dt, delta_dt)
    delta_ts: Timeseries = fetch_tolthawk_iv(site_id, delta_dt, now_dt)

    write_csv(f'../realtime/base/tolthawk-{site_id}.csv', base_ts)
    write_csv(f'../realtime/delta/tolthawk-{site_id}.csv', delta_ts)




