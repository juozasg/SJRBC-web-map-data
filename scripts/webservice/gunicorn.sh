#!/usr/bin/env bash

gunicorn -w 2 -b 0.0.0.0  'timeseries_api:app'