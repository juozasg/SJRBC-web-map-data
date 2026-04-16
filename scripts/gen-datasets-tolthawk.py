import requests
from datetime import datetime, timezone
import csv
import argparse
import os
from api.common import Timeseries
from api.tolthawk import tolthawk_valid_sensors, fetch_tolthawk_iv
import pytz
from datetime import timedelta


parser = argparse.ArgumentParser(description='Calculate and cache Tolthawk daily flow data in CSV format.')
parser.add_argument('datasets_dir', help='Directory where tolthawk.csv will be written.')
args = parser.parse_args()

datasets_dir = args.datasets_dir
output_path = os.path.join(args.datasets_dir, 'tolthawk.csv')

start_dt =  datetime(2022, 1, 1, 0, 0, tzinfo=pytz.utc)
now_dt = datetime.now(timezone.utc)

sites: dict[int, dict] = dict()

for sensor_id in tolthawk_valid_sensors:
# for sensor_id in [399]:
    # ts: Timeseries = fetch_tolthawk_iv(sensor_id, start_dt, now_dt)
    # Split [start_dt, now_dt] into 10 sections
    section_count = 5
    total_span = now_dt - start_dt
    section_span = total_span / section_count

    ts: Timeseries = []
    for i in range(section_count):
        section_start = start_dt + i * section_span
        section_end = now_dt if i == section_count - 1 else start_dt + (i + 1) * section_span

        ts_part: Timeseries = fetch_tolthawk_iv(sensor_id, section_start, section_end)
        ts.extend(ts_part)


    # datetime list of reeadings or average reading per dat
    sites[sensor_id]: dict[str, list[float] | float] = dict()
    for reading in ts:
        date_time = datetime.fromtimestamp(reading.timestamp, pytz.timezone('US/Eastern')).strftime('%Y-%m-%d')
        flow = reading.flow

        # print(sensor_id, date_time, reading)
        # exit(0)

        if date_time not in sites[sensor_id]:
            sites[sensor_id][date_time] = []

        sites[sensor_id][date_time].append(flow)


    # Calculate mean flow for each date
    for date, flows in sites[sensor_id].items():
        mean_flow = sum(flows) / len(flows)
        sites[sensor_id][date] = mean_flow

    print(sensor_id, len(ts), "IV readings", len(sites[sensor_id]), "daily means", "| total mean flow", sum(sites[sensor_id].values()) / (len(sites[sensor_id]) or 1))
    # sort dates
    sites[sensor_id] = dict(sorted(sites[sensor_id].items()))

with open(output_path, 'w', newline='') as csvfile:
    csv_writer = csv.writer(csvfile, lineterminator='\n')

    # Write header
    csv_writer.writerow(['siteId', 'date', 'flow'])
    # Write data rows
    for sensor_id, dates in sites.items():
        for date, flow in dates.items():
            csv_writer.writerow([f'tolthawk-{sensor_id}', date, flow])

    print(f"Data written to {output_path} for {len(sites)} sensors")



    # print(sites)
    # print("total days:", len(sites[sensor_id]))
    # exit(0)


    # print(sensor_status)
    # sensor_id = 1001  # Example sensor ID, replace with actual ID

