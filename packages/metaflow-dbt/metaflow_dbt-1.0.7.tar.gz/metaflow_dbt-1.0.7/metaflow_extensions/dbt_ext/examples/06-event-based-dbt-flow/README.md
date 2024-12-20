# Event based DBT Flow

This example shows how a DBT flow can be triggered with an event, and how parameters can be passed as part of the event in order to control DBT execution.

## Setup

Run the `./setup.sh` script and follow the instructions.

For our example we use AWS Secrets Manager for storing credentials to an RDS Postgres instance. You need to replace the values in `config.py` with the correct secret key, and db host.

## Running

First we deploy the flow which is responsible for listening to events and running the DBT project. This one listens to an event called `dbt_jaffle_demo`
```sh
python eventdbtflow.py --environment conda argo-workflows create
```

Then we can deploy and trigger a flow that sends a custom value for the `models` attribute as an event payload. This way we can customise the behaviour of the `@dbt` execution in the triggered flow.
```sh
python triggeringflow.py argo-workflows create
python triggeringflow.py argo-workflows trigger
```

The flow only works with `argo-workflow` due to relying on events.

Alternatively you can define a base Docker image that has the necessary requirements for executing DBT. You can try using the official DBT images as follows:

```sh
export METAFLOW_DEFAULT_CONTAINER_REGISTRY="ghcr.io/dbt-labs"
export METAFLOW_DEFAULT_CONTAINER_IMAGE="dbt-postgres:1.7.0"
python eventdbtflow.py argo-workflows create
```