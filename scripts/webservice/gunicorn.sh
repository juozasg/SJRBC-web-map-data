#!/usr/bin/env bash

gunicorn -w 2 -b 0.0.0.0:5003  'timeseries_api:app'