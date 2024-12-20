from metaflow import (
    step,
    FlowSpec,
)

from metaflow.plugins.argo.argo_events import ArgoEvent


class DBTEventFlow(FlowSpec):
    @step
    def start(self):
        print("Event broadcasting")

        event = ArgoEvent("dbt_jaffle_demo")

        # we want to set the "models" parameter for triggered flows to 'customers'
        event.publish(payload={"models": ["customers"]})
        self.next(self.end)

    @step
    def end(self):
        print("Done! 🏁")


if __name__ == "__main__":
    DBTEventFlow()
