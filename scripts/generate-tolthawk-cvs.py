import requests
from datetime import datetime, timezone
import csv

from api.common import Timeseries
from api.tolthawk import tolthawk_valid_sensors, fetch_tolthawk_iv
import pytz



start_dt =  datetime(2022, 7, 19, 0, 0, tzinfo=pytz.utc)
now_dt = datetime.now(timezone.utc)


start_dt =  datetime(2025, 7, 4, 0, 0, tzinfo=pytz.utc)
# now_dt =  datetime(2025, 7, 20, 0, 0, tzinfo=pytz.utc)




# Main execution
# TODO: collect all readings for each day and write mean water level to tolthawk.csv

sites: dict[int, dict] = dict()

for sensor_id in tolthawk_valid_sensors:
    ts: Timeseries = fetch_tolthawk_iv(sensor_id, start_dt, now_dt)

    # datetime list of reeadings or average reading per dat
    sites[sensor_id]: dict[str, list[float] | float] = dict()
    for reading in ts:
        date_time = datetime.fromtimestamp(reading.timestamp, pytz.timezone('US/Eastern')).strftime('%Y-%m-%d')
        flow = reading.flow

        print(sensor_id, date_time, reading)
        exit(0)

        if date_time not in sites[sensor_id]:
            sites[sensor_id][date_time] = []

        sites[sensor_id][date_time].append(flow)


    # Calculate mean flow for each date
    for date, flows in sites[sensor_id].items():
        mean_flow = sum(flows) / len(flows)
        sites[sensor_id][date] = mean_flow

    print(len(ts), "readings", len(sites[sensor_id]), "days", "| mean flow", sum(sites[sensor_id].values()) / (len(sites[sensor_id]) or 1))
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

