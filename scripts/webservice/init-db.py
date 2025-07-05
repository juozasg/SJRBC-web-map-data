# cache USGS NWIS daily data in CSV format under datasets

import csv
import os
from datetime import datetime, timezone, timedelta

import pytz

from api.common import Timeseries
from api.tolthawk import fetch_tolthawk_iv, tolthawk_valid_sensors
from api.usgs import fetch_usgs_iv


def write_csv(path, timeseries: Timeseries):
    with open(path, 'w', newline='') as csvfile:
        csv_writer = csv.writer(csvfile)
        csv_writer.writerow(['ts', 'flow'])
        for record in timeseries:
            csv_writer.writerow([record.timestamp, record.flow])
    print(f'Wrote {len(timeseries)} records to {path}')

file_dir = os.path.dirname(__file__)

os.makedirs(file_dir + '/realtime-db', exist_ok=True)


start_dt =  datetime(2023, 3, 1, 0, 0, tzinfo=pytz.utc)
# start_dt =  datetime(2025, 7, 1, 0, 0, tzinfo=pytz.utc)
# delta_dt = datetime(2025, 7, 1, 0, 0, tzinfo=pytz.utc)
now_dt = datetime.now(timezone.utc)
print(now_dt, now_dt.timestamp())

usgs_ids = ['04096405', '04096515', '04097500', '040975299', '04097540', '04099000', '04100500', '04101000', '04101500', '04101800', '04102500', '04099750']
for site_id in usgs_ids:
    base_ts: Timeseries = fetch_usgs_iv(site_id, start_dt, now_dt)


    write_csv(f'{file_dir}/realtime-db/usgs-{site_id}.csv', base_ts)

tt_ids = tolthawk_valid_sensors
for site_id in tt_ids:
    base_ts: Timeseries = fetch_tolthawk_iv(site_id, start_dt, now_dt)

    write_csv(f'{file_dir}/realtime-db/tolthawk-{site_id}.csv', base_ts)




