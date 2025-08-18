#!/usr/bin/env bash

gunicorn -w 2 -b 0.0.0.0:5003 --certfile=server.crt --keyfile=server.key  'timeseries_api:app'