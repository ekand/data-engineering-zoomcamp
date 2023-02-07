Docker  
delivers software in packages called containers  
isolate data pipelines  
Host computer   
Container:  
- Ubuntu 20.02
- Python 3.9
- Pandas
- Postgres connection library
Container:
- Postgres
Separated from postgres on Host computer  

Another advantage: Reproducibility  
eg: put same container on Google cloud

If it works on my computer...

Reasons to care about Docker
- Reproducibility
- Local Experiments
- Integration tests (CI/CD)
- Running pipelines on the cloud
- Spark
- Serverless (AWS Lambda)

```bash
docker run hello-world
```

```bash
docker run -it ubuntu bash
```

```bash
docker run -it python:3.9
```

```python
>>> import pandas
```

```bash
docker run -it --entrypoint=bash python:3.9
```

```shell
pip install pandas
python
```

```Dockerfile
FROM python:3.9

RUN pip install pandas

ENTRYPOINT [ "bash" ]
```

```bash
docker build -t test:pandas .
```

Caching

```bash
docker run -it test:pandas
```

```python
import pandas
```

```Dockerfile
FROM python:3.9

RUN pip install pandas

WORKDIR /app
COPY pipeline.py pipeline.py

ENTRYPOINT [ "bash" ]
```

```shell
docker build -t test:pandas .
```

```Dockerfile
FROM python:3.9

RUN pip install pandas

WORKDIR /app
COPY pipeline.py pipeline.py

ENTRYPOINT [ "python", "pipeline.py" ]
```

pipeline.py
```python
import sys

import pandas as pd

print(sys.argv)

day = sys.argv[1]

# some fancy stuff with pandas

print(f'job finished successfully for day = {day}')
```

```shell
docker build -t test:pandas .
docker run -it test:pandas friday
```
