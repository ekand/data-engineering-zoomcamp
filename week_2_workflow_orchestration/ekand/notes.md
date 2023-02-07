# Week 2: Workflow Orchestration

## Video: De Zoomcamp 2.1.1 - Data Lake

holds big data

ingest data and make it accessible

metadata for faster access

secure

can scale

inexpensive hardware

vs data warehouse

data lake unstructured / data warehouse structured

how did it start?

ETL vs ELT

ELT corresponds with datalake

gotchas

data swamp

lack of versioning

incompatible schemas

## Video: DE Zoomcamp 2.2.1 - Introduction to Workflow orchestration

workflow orchestration

analogy to a delivery system

## Video: DE Zoomcamp 2.2.2 - Introduction to Prefect Concepts

ingest data.py

transform it to be orchestrated with Prefect

create and activate python environment

`pip install -r requirements.txt`

`prefect version`

`from prefect import flow, task`

a flow is the most basic Python object in Prefect

use the `@flow` decorator on a function

a flow can contain a task

tasks can receive metadata about upstream dependencies

task can have `log_prints` and `retries`. 

running a flow

refactoring into more functions

caching tasks

`from prefect.tasks import task_input_hash`

`cache_key_fn=task_input_hash`

`cache_expiration=timedelta(days=2)`

transforming data

load data into postgres

parameterization and subflows

flows can contain other flows

orion ui

blocks

notifications

blocks are a primitive within prefect. stores configuration. lets you interact with external systems.

connector

`from prefect_sqlalchemy import SqlAlchemyConnector`

`with connection_block.get_connection(begin=False) as engine:`

## Video: DE Zoomcamp 2.2.3 - ETL with GCP & Prefect

moving prefect to the cloud

activate environment 'zoom'

`prefect orion start`

etl_web_to_gcs.py

`from pathlib import path`  
`import pandas as pd`  
`from prefect import flow, task`  
`from prefect_gcp.cloud_storage import BcsBucket`  

```python

@task(retries=3)
def fetch(dataset_url: str) -> pd.DataFrame:
    """Read taxi data from web into pandas DataFrame"""
    # if randint(0, 1) > 0:
        # raise Exception
    df = pd.read_csv(dataset_url)
    return df

@task(log_prints=True)
def clean(df:pd.DataFrame) -> pd.DataFrame:
    """Fix dtype issues"""
    df['tpep_pickup_datetime'] = pd.to_dateatime(df['tpep_pickup_datetime'])
    df['tpep_dropoff_datetime'] = pd.to_dateatime(df['tpep_dropoff_datetime'])
    print(df.head(2))
    print(f"columns: {df.dtypes}")
    print(f"rows: {len(df)}")

@task()
def write_local(clean_df: pd.DataFrame, color: str, dataset_file: str) -> Path:
    """Write DataFrame out locally as parquet file"""
    path = Path(f"data/{color}/{dataset_file}.parquet")
    clean_df.to_parquet(path, compression="gzip")
    return path

@task()
def write_to_gcs(path: Path) -> None:
    """Upload local parquet file to GCS"""
    gcs_block = GcsBucket.load("zoom-gcs")
    gcs_block.upload_from_path(
        from_path=f"{path}",
        to_path=path
    )


@flow()
def etl_web_to_gcs() -> None:
    """The main ETL function"""
    color = "yellow"
    year = 2021
    month = 1
    dataset_file = f"{color}_tripdata_{year}-{month:01}"
    dataset_url = f"https://github.com/..."

    df = fetch(dataset_url)
    df_clean = clean(df)
    write_local(df_clean, color, dataset_file)




if __name__ == '__main__':
    etl_web_to_gcs()    
```




`$ prefect block register`

orion ui: looking at blocks

service account on GCP

add a GCP credentials block to the GCS bucket block

## Video: DE Zoomcamp 2.2.4 From Google Cloud Storage to Big Query

etl_gcs_to_bq.py
```python
from pathlib import Path
import pandas as pd
from prefect import flow, task
from prefect_gcp.cloud_storage import GcsBucket
from prefect_gcp import GcpCredentials

@task(retries=3)
def extract_from_gcs(color: str, year: int, month: int) -> Path:
    """Download trip data from GCS"""
    gcs_path = f"data/{color}/{color}_tripdata_{year}-{month:-2}.parquet"
    gcs_block = GcsBucket.load("zoom-gcs")
    gcs_block.get_directory(from_path=gcs_path, local_path=f"../data/")
    return = Path(f"../data/{gcs_path}")

@task()
def transform(path: Path) -> pd.DataFrame:
    """Data cleaning example"""
    df = pd.read_parquet(path)
    print(f"pre:missing passenger count: {df['passenger_count'].isna().sum()}")
    df['passenger_count'].fillna(0, inplace=True)
    print(f"post:missing passenger count: {df['passenger_count'].isna().sum()}")
    return df

@task
def write_bq(df: pd.DataFrame) -> None:
    """Write DataFrame to BigQuery"""

    gcp_credentials_block = GcpCredentials.load("zoom-gcp-creds")
    df.to_gbq(
        destination="dezoomcamp.rides"
        project_id="prefect-sbx-community-eng"
        credentials=gcp_credentials_block.get_credentials_from_service_account(),
        chucksize=500_000
        if_exist=append
    )
@flow()
def etl_gcs_to_bq():
    """Main ETL flow to load data """
    color = "yellow"
    year = 2021
    month = 1

    path = extract_from_gcs(color, year, month)
    df = transform(path)
    write_bq(df)

if __name__ == '__main__':
    etl_gcs_to_bq()
```

gbc web ui, loading table from gcs

delete from the table (leaving just the schema)

run the flow

query to select data

## Video: DE Zoomcamp 2.2.5 - Parametrizing Flow & Deployments with ETL into GCS flow

parameterized_flow.py
```python

from pathlib import path
import pandas as pd
from prefect import flow, task
from prefect_gcp.cloud_storage import BcsBucket
from prefect.tasks import task_input_hash
from datetime import timedelta

@task(retries=3, cache_key_fn=task_input_hash, cache_expiration=timedelta(days=1))
def fetch(dataset_url: str) -> pd.DataFrame:
    """Read taxi data from web into pandas DataFrame"""
    # if randint(0, 1) > 0:
        # raise Exception
    df = pd.read_csv(dataset_url)
    return df

@task(log_prints=True)
def clean(df:pd.DataFrame) -> pd.DataFrame:
    """Fix dtype issues"""
    df['tpep_pickup_datetime'] = pd.to_dateatime(df['tpep_pickup_datetime'])
    df['tpep_dropoff_datetime'] = pd.to_dateatime(df['tpep_dropoff_datetime'])
    print(df.head(2))
    print(f"columns: {df.dtypes}")
    print(f"rows: {len(df)}")

@task()
def write_local(clean_df: pd.DataFrame, color: str, dataset_file: str) -> Path:
    """Write DataFrame out locally as parquet file"""
    path = Path(f"data/{color}/{dataset_file}.parquet")
    clean_df.to_parquet(path, compression="gzip")
    return path

@task()
def write_to_gcs(path: Path) -> None:
    """Upload local parquet file to GCS"""
    gcs_block = GcsBucket.load("zoom-gcs")
    gcs_block.upload_from_path(
        from_path=f"{path}",
        to_path=path
    )


@flow()
def etl_web_to_gcs(color: str, year: int, month: int) -> None:
    """The main ETL function"""
    dataset_file = f"{color}_tripdata_{year}-{month:01}"
    dataset_url = f"https://github.com/..."

    df = fetch(dataset_url)
    df_clean = clean(df)
    write_local(df_clean, color, dataset_file)

#parent flow
@flow()
def etl_parent_flow(
    months: list[int]=[1, 2],
    year: int = 2021,
    color: str = "yellow"
):
    for month in months:
        etl_web_to_gcs(year, month, color)


if __name__ == '__main__':
    color = "yellow"
    months = [1, 2, 3]
    year = 2021
    etl_parent_flow(months, year, color)    
```

add parent flow

add caching to a task

run it `python parameterized_flow.py`

follow along in orion ui

a deployment in Prefect

build a deployment through the cli

`prefect deployment build ./parameterized_flow.py:etl_parent_flow -n "Parameterized ETL"`

adding parameters to `etl_parent_flow-deployment.yaml`

etl_parent_flow-deployment.yaml:
```yaml
...
parameters: {"color": "yellow", "months": [1, 2, 3], "year": 2021}
...
```

`prefect deployment apply etl_parent_flow-deployment.yaml`

you need an agent to execute flows

view and edit a deployment in the orion UI.

quick run or custom run

work queues and agents

`prefect agent start --work-queue "default"`

notifications: in orion web UI or in Python code

## DE Zoomcamp 2.2.6 - Schedule & Docker Storage with Infrastructure

running a deployment every 5 minutes

Interval, Cron, or RRule

`prefect deployment build flows/03_deployments/parameterized_flow.py:etl_parent_flow -n "etl2" --cron "0 0 * * *" -a`

`prefect deployment build --help`

`prefect deployment --help`

Running flows in Docker containers

so far, our code has been sitting locally on our machine

we could put it on github etc, S3, GCS, Azure blob storage, etc...

We are going to store our code on a Docker container, with an image on Docker Hub.

docker-requirements.txt
```requirements.txt
pandas==1.5.2
prefect-gcp[cloud_storage]==0.2.3
protobuf=4.21.11
pyarrow=10.0.1
```

Dockerfile
```Dockerfile
FROM prefecthq/prefect:2.7.7-python3.9

COPY docker-requirements.txt .

RUN pip install -r docker-requirements.txt --trusted-host pypi.python.org --no-cache-dir

COPY flows /opt/prefect/flows
COPY data /opt/prefect/data
```

`docker image build -t discdiver/prefect:zoom .`

log into docker hub

`docker image push discdiver/prefect:zoom`

Make a docker block in Orion  
Image: discdiver/prefect:zoom  
ImagePullPolicy: always
AutoRemote: True

could also use Python code to make a docker block

make a deployment. this time from a python file

docker_deploy.py   (in same directory as parameterized_flow.py)
```python
from prefect.deployments import Deployment
from prefect.infrastructure.docker import DockerContainer
from parameterized_flow import etl_parent_flow

docker_block = CockerContainer.load("zoom")

docker_dep = Deployment.build_from_flow(
    flow=etl_parent_flow,
    name="docker-flow",
    infrastructure=docker_block
)
if __name__ == "__main__":
    docker_dep.apply()
```

`python flows/03_deployments/docker_deploy.py`

`prefect profile ls`

`prefect config set PRFECT_API_URL="HTTP://127.0.0.1:4200/api"`

allows docker container to interface with the orion server

new terminal:  
`prefect agent start -q default` 

`prefect deployment run etl-parent-flow/docker-flow -p "months=[1,2]"`

watch this in the UI

we have brought our code to a docker image, put it on docker hub, and run that code in docker containers on a local machine

## Video: DE Zoomcamp 2.2.7 - Prefect Cloud/Additional Resources

additional resources

docs.prefect.io

hosted cloud

anna-geller on github

prefect discourse

prefect slack