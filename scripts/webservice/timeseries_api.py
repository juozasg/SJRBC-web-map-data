import os

from flask import Flask, Response, jsonify, request
import glob
import csv

import uuid

file_dir = os.path.dirname(__file__)
sites_timeseries = {}

app = Flask(__name__)

@app.route('/debug')
def debug_info():
    return file_dir

@app.route('/reload-database')
def load_csv_db():
    # Get all CSV files in the realtime-db folder
    csv_pattern = os.path.join(file_dir, 'realtime-db', '*.csv')
    csv_files = glob.glob(csv_pattern)

    # Process each CSV file
    for csv_file in csv_files:
        # Extract sensor_id from filename (remove .csv extension)
        sensor_id = os.path.basename(csv_file)[:-4]

        # Read the CSV file
        with open(csv_file, 'r') as f:
            csv_reader = csv.reader(f)
            # Store all lines for this sensor
            sites_timeseries[sensor_id] = list(csv_reader)
    return "OK"


@app.route('/timeseries-since/<sensor_id>/<int:timestamp>')
def get_timeseries_csv(sensor_id, timestamp):
    # path = f'{file_dir}/realtime-db/{sensor_id}.csv'
    if not sensor_id in sites_timeseries:
        return f"Not found {sensor_id}.csv"
    all_timeseries = sites_timeseries[sensor_id]
    since_timeseries = []

    for i in range(len(all_timeseries) - 1, 1, -1):
        ts = all_timeseries[i]
        stamp = int(ts[0])
        if stamp > timestamp:
            since_timeseries.append(ts)
        else:
            break

    # add the header
    since_timeseries.append(all_timeseries[0])
    since_timeseries.reverse()
    csv_rows = [','.join(row) for row in since_timeseries]
    csv_text = '\n'.join(csv_rows)
    return Response(csv_text, mimetype='text', headers={'Access-Control-Allow-Origin': '*'})


load_csv_db()

if __name__ == '__main__':
    app.run(debug=True)
    # print(sites_timeseries)
