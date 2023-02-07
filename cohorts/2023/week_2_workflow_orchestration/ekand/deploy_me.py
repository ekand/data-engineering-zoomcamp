from prefect.deployments import Deployment
from prefect.infrastructure.docker import DockerContainer
from etl_gcs_to_bq import parent_etl_flow
from prefect.filesystems import GitHub

github_block = GitHub.load("my-github-block")

docker_dep = Deployment.build_from_flow(
    flow=parent_etl_flow,
    name="docker-flow",
    filesystems=github_block
)
if __name__ == "__main__":
    docker_dep.apply()