import pandas as pd
from sqlalchemy import create_engine
from time import time
import argparse
import os


def main(params):
    user = params.user
    password = params.password
    host = params.host
    port = params.port
    db = params.db
    table = params.table
    url = params.url

    csv_name = 'output.csv'

    os.system(f"wget {url} -O {csv_name}.gz")
    os.system(f"gunzip {csv_name}.gz")

    df = pd.read_csv(csv_name, nrows=100)

    df.tpep_pickup_datetime = pd.to_datetime(df.tpep_pickup_datetime)
    df.tpep_dropoff_datetime = pd.to_datetime(df.tpep_dropoff_datetime)


    engine = create_engine(f'postgresql://{user}:{password}@{host}:{port}/{db}')

    print(pd.io.sql.get_schema(df, table, con=engine))


    df_iter = pd.read_csv(csv_name, iterator=True, chunksize=100000)

    first = True
    while True:
        t_start = time()
        df = next(df_iter)
        if first:
            df.head(0).to_sql(name=csv_name, con=engine, if_exists='replace')
            first = False
        df.tpep_pickup_datetime = pd.to_datetime(df.tpep_pickup_datetime)
        df.tpep_dropoff_datetime = pd.to_datetime(df.tpep_dropoff_datetime)
        df.to_sql(name='yellow_taxi_data', con=engine, if_exists='append')
        
        t_end = time()
        
        print('inserted another chunk..., took %.3f second' % (t_end - t_start))


if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='Ingest CSV data to Postgres')

    # user, password, host, port, dbname, tablename, url of the csv
    parser.add_argument('--user', help='user name for postgres')
    parser.add_argument('--password', help='password for postgres')
    parser.add_argument('--host', help='host for postgres')
    parser.add_argument('--port', help='port for postgres')
    parser.add_argument('--db', help='database name for postgres')
    parser.add_argument('--table', help='table name for postgres')
    parser.add_argument('--url', help='url source for data')

    args = parser.parse_args()

    main(args)
