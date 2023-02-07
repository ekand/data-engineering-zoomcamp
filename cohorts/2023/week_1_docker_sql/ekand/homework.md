## Week 1 Homework

In this homework we'll prepare the environment 
and practice with Docker and SQL


## Question 1. Knowing docker tags

Run the command to get information on Docker 

```docker --help```

Now run the command to get help on the "docker build" command

Which tag has the following text? - *Write the image ID to the file* 

- `--imageid string`
- `--iidfile string`  * * *
- `--idimage string`
- `--idfile string`


## Question 2. Understanding docker first run 

Run docker with the python:3.9 image in an interactive mode and the entrypoint of bash.
Now check the python modules that are installed ( use pip list). 
How many python packages/modules are installed?

pip, setuptools, wheel

- 1
- 6
- 3 * * *
- 7

# Prepare Postgres

Run Postgres and load data as shown in the videos
We'll use the green taxi trips from January 2019:

```wget https://github.com/DataTalksClub/nyc-tlc-data/releases/download/green/green_tripdata_2019-01.csv.gz```

You will also need the dataset with zones:

```wget https://s3.amazonaws.com/nyc-tlc/misc/taxi+_zone_lookup.csv```

Download this data and put it into Postgres (with jupyter notebooks or with a pipeline)


## Question 3. Count records 

How many taxi trips were totally made on January 15?

Tip: started and finished on 2019-01-15. 

Remember that `lpep_pickup_datetime` and `lpep_dropoff_datetime` columns are in the format timestamp (date and hour+min+sec) and not in date.

```
-- select count(*) from green_taxi_data
-- where lpep_pickup_datetime::date='2019-01-15'::date
-- and lpep_dropoff_datetime::date='2019-01-15'::date;
```

- 20689
- 20530 * * *
- 17630
- 21090

## Question 4. Largest trip for each day

Which was the day with the largest trip distance
Use the pick up time for your calculations.

```
select lpep_pickup_datetime, trip_distance from 
green_taxi_data
order by trip_distance desc
limit 1;
```

- 2019-01-18
- 2019-01-28
- 2019-01-15 * * *
- 2019-01-10

## Question 5. The number of passengers

In 2019-01-01 how many trips had 2 and 3 passengers?
 
```select count(*) from green_taxi_data where 
lpep_pickup_datetime::date = '2019-01-01'::date
and passenger_count=3;
```

- 2: 1282 ; 3: 266
- 2: 1532 ; 3: 126
- 2: 1282 ; 3: 254  * * *
- 2: 1282 ; 3: 274


## Question 6. Largest tip

For the passengers picked up in the Astoria Zone which was the drop off zone that had the largest tip?
We want the name of the zone, not the id.

Note: it's not a typo, it's `tip` , not `trip`

```
select zdo."Zone", max(tip_amount) AS max_tip
from green_taxi_data
inner join taxiplus_zone_lookup zpu
on green_taxi_data."PULocationID" = zpu."LocationID"
inner join taxiplus_zone_lookup zdo
on green_taxi_data."DOLocationID" = zdo."LocationID"
where zpu."Zone"='Astoria'
group by zdo."Zone"
order by max_tip desc
limit 1
;
```

- Central Park
- Jamaica
- South Ozone Park
- Long Island City/Queens Plaza * * *


## Submitting the solutions

* Form for submitting: [form](https://forms.gle/EjphSkR1b3nsdojv7)
* You can submit your homework multiple times. In this case, only the last submission will be used. 

Deadline: 30 January (Monday), 22:00 CET


## Solution

See here: https://www.youtube.com/watch?v=KIh_9tZiroA
