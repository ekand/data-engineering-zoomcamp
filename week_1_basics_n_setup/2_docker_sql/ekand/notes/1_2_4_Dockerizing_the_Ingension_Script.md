# Dockerizing the Ingestion Script

see ../2_docker_sql/ingest_data.py

URL=

```shell
python ingest_data.py \
  --user=root \
  --password=root \
  --host=localhost \
  --port=5432 \
  --db=ny_taxi \
  --table=yellow_taxi_trips
  --url=${URL}