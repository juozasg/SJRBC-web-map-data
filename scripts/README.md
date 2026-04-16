# SJRBC data scripts

`init-python.sh` creates the venv and installs deps

Run `. .venv/bin/activate` to activate the python venv.

### build-indexes.py
Builds `indexes` data with spatial indexes to get a list of sites contained in each of the polygon features (catchments, HUCs, etc).

### Tolthawk and USGS daily datasets
`gen-datasets-tolthawk.py` and `gen-datasets-usgs.py` scripts add regular daily timeseries to the `datasets` folders for these two web APIs. USGS daily values are used for `flow`, `temp`, `height`, `do` variables as are available. For Tolthawk 15 minute API `height` values are averaged and applied to discharge curves (in `tolthawk.py`) to create daily `flow` values.

For days before 2022-01-01 only the dates that contain dataset records are used. This is determined by `dates_that_have_records.py`

`tolthawk-login.py` will read the file `tolkhawk-login` that contains email and password as 2 lines and will create `tolthawk-token` file used to authenticate with the tolthawk API.

### Reatime Tolthawk and USGS

Realtime (15 min) instantenous values (IV) data is provided to the client with several layers of caching. `realtime/base` and `realtime/delta` folders contain segments of the full timeseries for each site. `base` segments should never be updated (always cached for the client) while `delta` segments can be updated whenever needed by rebuilding the files and pushing to git. `gen-realtime-base-delta.py` builds both `base` and `delta` files. `base` generation code should be commented out normally.



#### Realtime webservice
Finally, there is a real-time component for data segments not packaged here. `scripts/webservice` contains code for creating and updating the realtime caching and serving it with `gunicorn`

`api/tolthawk-login.sh` and `webservice/update-db.sh` should be added to cron for the webservice to work:


```aiignore
    */15 * * * * /somewhere/SJRBC-web-map-data/scripts/webservice/update-db.sh
    1 1 * * 1 /somewhere/SJRBC-web-map-data/scripts/api/tolthawk-login.sh
```

`sjrbc-gunicorn.service` runs the webservice on systemd. Update the file with your USERNAME, GROUP and deployment path and install:

```aiignore
    cp sjrbc-gunicorn.service /etc/systemd/system/
    systemctl enable sjrbc-gunicorn
    systemctl start sjrbc-gunicorn
```

Run `scripts/webservice/init-db.sh` to initialize the timeseries database for the service


#### Webservice SSL

SSL is required and can be provided by LetsEncrypt. Crontab to renew the cert:

```
1 1 * * 2 sudo certbot renew
```


#### Testing the webservice

`curl https://timeseries.riverdata.app:5003/timeseries-since/tolthawk-392/1776312948`

#### Timestamps

Timestamp conversion to datetime: https://www.epochconverter.com