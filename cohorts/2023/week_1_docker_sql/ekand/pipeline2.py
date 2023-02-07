import pandas as pd
from time import time
from sqlalchemy import create_engine
# import psycopg2


df = pd.read_csv('_gitignore/data/taxi+_zone_lookup.csv', nrows=100)

# df.lpep_pickup_datetime = pd.to_datetime(df.lpep_pickup_datetime)
# df.lpep_dropoff_datetime = pd.to_datetime(df.lpep_dropoff_datetime)

engine = create_engine('postgresql://root:root@localhost:5432/ny_taxi')

df.head(0).to_sql(name='taxiplus_zone_lookup', con=engine, if_exists='replace')

df_iter = pd.read_csv('_gitignore/data/taxi+_zone_lookup.csv', iterator=True, chunksize=100000)
while True:
    t_start = time()
    df = next(df_iter)
    # df.lpep_pickup_datetime = pd.to_datetime(df.lpep_pickup_datetime)
    # df.lpep_dropoff_datetime = pd.to_datetime(df.lpep_dropoff_datetime)
    df.to_sql(name='taxiplus_zone_lookup', con=engine, if_exists='append')
    
    t_end = time()
    
    print('inserted another chunk..., took %.3f second' % (t_end - t_start))

