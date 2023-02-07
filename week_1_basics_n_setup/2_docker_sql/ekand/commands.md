```
URL="https://github.com/DataTalksClub/nyc-tlc-data/releases/download/yellow/yellow_tripdata_2019-01.csv.gz"
```

```
docker build -t taxi_ingest:v0 .
```

```shell
docker run -it \
  --network=pg-network \
  taxi_ingest:v0 \
    --user=root \
    --password=root \
    --host=pg-database \
    --port=5432 \
    --db=ny_taxi \
    --table=yellow_taxi_trips \
    --url=${URL}

```