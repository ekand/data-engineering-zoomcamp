# 1.2.2 - Ingesting NY Taxi Data to Postgres

We will run Postgres in Docker

```
docker run -it \
  -e POSTGRES_USER="root" \
  -e POSTGRES_PASSWORD="root" \
  -e POSTGRES_DB="ny_taxi" \
  -v  /Users/erik/workspace/github.com/ekand/dezoomcamp/ny_taxi_postgres_data:/var/lib/postgresql/data \
  -p 5432:5432 \
  postgres:13
```
-v for mounting
-p for port


```shell
pgcli -h localhost -p 5432 -u root -d ny_taxi
```
(type password 'root' for root)

Aside: I needed
`brew install postgresql`



## Dataset for the course

Jupyter Notebook.

```python
import pandas
```

```shell
wget https://github.com/DataTalksClub/nyc-tlc-data/releases/download/yellow/yellow_tripdata_2019-01.csv.gz
```

## Optional adendum: Connecting to Postgres with Jupyter and Pandas



### Setup connection

```python
import pandas as pd
import sqlalchemy

engine = create_engine('postgresql://root:root@localhost:5432/ny_taxi')
```

### Run basic SQL query
```python
query = """
SELECT 1 as number
"""
pd.read_sql(query, con=engine)
```

### List tables with SQL query

```python
query = """
SELECT *
FROM pg_catalog.pg_tables
WHERE schemaname != 'pg_catalog' AND
 schemaname != 'information_schema'

"""
pd.read_sql(query, con=engine)
```

### Load data into table

```python
df = pd.read_csv('yellow_tripdata_2019-01.csv', nrows=100)
df.tpep_pickup_datetime = pd.to_datetime(df.tpep_pickup_datetime)
df.tpep_dropoff_datetime = pd.to_datetime(df.tpep_dropoff_datetime)
df.to_sql(name='yellow_tripdata_trip', con=engine, index=False)
```

### View data

```python
query = """
SELECT *
FROM yellow_tripdata_trip limit 10

"""
pd.read_sql(query, con=engine)
```