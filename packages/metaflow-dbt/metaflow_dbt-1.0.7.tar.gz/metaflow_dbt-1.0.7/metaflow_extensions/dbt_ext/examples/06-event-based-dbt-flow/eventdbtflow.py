from metaflow import (
    conda_base,
    step,
    FlowSpec,
    dbt,
    environment,
    secrets,
    trigger,
    Parameter,
    JSONType,
)
from config import DBT_PROFILES, SECRET_SRC, HOST_ENV


@conda_base(packages={"dbt-postgres": ">=1.7.0"})
@trigger(event="dbt_jaffle_demo")
class EventTriggeredDBTFlow(FlowSpec):
    models = Parameter(name="models", default=["orders"], type=JSONType)

    @step
    def start(self):
        print("Start step for debugging")
        self.next(self.jaffle_seed)

    @dbt(
        command="seed",
        project_dir="./jaffle_shop",
        profiles=DBT_PROFILES,
    )
    @secrets(sources=SECRET_SRC)
    @environment(vars=HOST_ENV)
    @step
    def jaffle_seed(self):
        # jaffle_shop example needs to be seeded before 'dbt run' works for its models.
        print("Seeded jaffle_shop")
        self.next(self.jaffle_models)

    @dbt(
        models=models,
        project_dir="./jaffle_shop",
        profiles=DBT_PROFILES,
        generate_docs=True,
    )
    @secrets(sources=SECRET_SRC)
    @environment(vars=HOST_ENV)
    @step
    def jaffle_models(self):
        print(f"jaffle_shop DBT run: {self.models}")
        self.next(self.end)

    @step
    def end(self):
        print("Done! 🏁")


if __name__ == "__main__":
    EventTriggeredDBTFlow()
