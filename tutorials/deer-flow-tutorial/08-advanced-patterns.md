---
layout: default
title: "Chapter 8: Advanced Patterns"
parent: "Deer Flow Tutorial"
nav_order: 8
---

# Chapter 8: Advanced Patterns

> Master sophisticated orchestration patterns for complex workflow scenarios.

## Overview

This chapter covers advanced workflow patterns including dynamic workflows, event-driven architectures, sub-workflows, and complex orchestration scenarios that solve real-world distributed system challenges.

## Dynamic Workflows

### Runtime Task Generation

```python
from deerflow import Workflow, DynamicTasks

workflow = Workflow(name="dynamic_etl")

@workflow.task(id="discover_sources")
def discover_sources(context):
    """Discover data sources at runtime."""
    sources = list_s3_buckets(prefix="data-")
    return {"sources": sources}

@workflow.dynamic_tasks(id="process_sources", depends_on=["discover_sources"])
def generate_processing_tasks(context):
    """Generate a task for each discovered source."""
    sources = context.tasks["discover_sources"].output["sources"]

    tasks = []
    for source in sources:
        tasks.append({
            "id": f"process_{source['name']}",
            "type": "python",
            "config": {
                "script": "process_source.py",
                "args": [source["uri"]]
            }
        })

    return tasks

@workflow.task(id="aggregate", depends_on=["process_sources"])
def aggregate_results(context):
    """Aggregate results from all dynamic tasks."""
    results = []
    for task_id, output in context.dynamic_outputs["process_sources"].items():
        results.append(output)
    return {"total_records": sum(r["count"] for r in results)}
```

### Parameterized Workflow Templates

```python
from deerflow import WorkflowTemplate

template = WorkflowTemplate(
    name="data_pipeline_template",
    parameters={
        "source_type": {"type": "string", "enum": ["s3", "gcs", "azure"]},
        "destination": {"type": "string"},
        "parallelism": {"type": "integer", "default": 5}
    }
)

@template.task(id="extract")
def extract(context):
    source_type = context.params["source_type"]
    # Extract based on source type
    pass

@template.task(id="transform", depends_on=["extract"])
def transform(context):
    pass

@template.task(id="load", depends_on=["transform"])
def load(context):
    destination = context.params["destination"]
    pass

# Instantiate for different configurations
s3_pipeline = template.instantiate(
    name="s3_to_warehouse",
    parameters={"source_type": "s3", "destination": "snowflake"}
)

gcs_pipeline = template.instantiate(
    name="gcs_to_warehouse",
    parameters={"source_type": "gcs", "destination": "bigquery"}
)
```

## Sub-Workflows

### Nested Workflows

```python
from deerflow import Workflow, SubWorkflow

# Define reusable sub-workflow
validation_workflow = Workflow(name="data_validation")

@validation_workflow.task(id="schema_check")
def check_schema(context):
    return validate_schema(context.input)

@validation_workflow.task(id="quality_check", depends_on=["schema_check"])
def check_quality(context):
    return validate_quality(context.input)

# Main workflow using sub-workflow
main_workflow = Workflow(name="etl_with_validation")

@main_workflow.task(id="extract")
def extract(context):
    return fetch_data()

@main_workflow.sub_workflow(
    id="validate",
    workflow=validation_workflow,
    depends_on=["extract"]
)

@main_workflow.task(id="transform", depends_on=["validate"])
def transform(context):
    validated_data = context.tasks["validate"].output
    return transform_data(validated_data)
```

### Workflow Composition

```python
from deerflow import compose_workflows

# Compose multiple workflows
composed = compose_workflows(
    name="full_pipeline",
    workflows=[
        {"workflow": "extraction_workflow", "alias": "extract"},
        {"workflow": "transformation_workflow", "alias": "transform", "depends_on": ["extract"]},
        {"workflow": "loading_workflow", "alias": "load", "depends_on": ["transform"]}
    ],
    connections={
        "transform.input": "extract.output",
        "load.input": "transform.output"
    }
)
```

## Event-Driven Patterns

### Event Triggers

```python
from deerflow import Workflow, EventTrigger
from deerflow.events import S3Event, KafkaEvent, WebhookEvent

workflow = Workflow(name="event_driven_pipeline")

# S3 event trigger
workflow.add_trigger(
    S3Event(
        bucket="data-lake",
        prefix="incoming/",
        events=["s3:ObjectCreated:*"],
        filter={"suffix": ".parquet"}
    )
)

# Kafka event trigger
workflow.add_trigger(
    KafkaEvent(
        topic="data-events",
        consumer_group="deerflow",
        filter=lambda msg: msg["type"] == "new_data"
    )
)

# Webhook trigger
workflow.add_trigger(
    WebhookEvent(
        path="/trigger/pipeline",
        method="POST",
        auth="api_key"
    )
)

@workflow.task(id="process_event")
def process_event(context):
    event = context.trigger_event
    if event.type == "s3":
        return process_s3_file(event.bucket, event.key)
    elif event.type == "kafka":
        return process_kafka_message(event.message)
```

### Event Sourcing Pattern

```python
from deerflow import Workflow, EventStore

event_store = EventStore(backend="kafka", topic="workflow-events")

workflow = Workflow(name="event_sourced_order")

@workflow.task(id="create_order")
def create_order(context):
    order = {"id": uuid4(), "items": context.params["items"]}

    # Publish event
    event_store.publish({
        "type": "OrderCreated",
        "payload": order,
        "timestamp": datetime.utcnow()
    })

    return order

@workflow.task(id="process_payment", depends_on=["create_order"])
def process_payment(context):
    order = context.tasks["create_order"].output

    result = charge_payment(order)

    event_store.publish({
        "type": "PaymentProcessed",
        "payload": {"order_id": order["id"], "status": result["status"]},
        "timestamp": datetime.utcnow()
    })

    return result
```

## Saga Pattern

### Distributed Transactions

```python
from deerflow import Workflow, Saga, CompensatingAction

workflow = Workflow(name="order_saga")

@workflow.saga
class OrderSaga(Saga):
    @step(order=1)
    def reserve_inventory(self, context):
        return inventory_service.reserve(context.params["items"])

    @step(order=1, compensate="release_inventory")
    def release_inventory(self, context, reservation):
        inventory_service.release(reservation["id"])

    @step(order=2)
    def charge_payment(self, context):
        return payment_service.charge(
            context.params["customer_id"],
            context.params["amount"]
        )

    @step(order=2, compensate="refund_payment")
    def refund_payment(self, context, payment):
        payment_service.refund(payment["id"])

    @step(order=3)
    def create_shipment(self, context):
        return shipping_service.create_shipment(
            context.params["address"],
            context.tasks["reserve_inventory"].output["items"]
        )

    @step(order=3, compensate="cancel_shipment")
    def cancel_shipment(self, context, shipment):
        shipping_service.cancel(shipment["id"])
```

### Choreography vs Orchestration

```python
# Orchestration (centralized control)
orchestrated_workflow = Workflow(name="orchestrated_order")

@orchestrated_workflow.task(id="coordinator")
async def coordinate_order(context):
    # Central coordinator manages all steps
    inventory = await call_inventory_service(context.params)
    payment = await call_payment_service(context.params)
    shipping = await call_shipping_service(context.params)
    return {"inventory": inventory, "payment": payment, "shipping": shipping}

# Choreography (event-driven, decentralized)
choreographed_workflow = Workflow(name="choreographed_order")

@choreographed_workflow.task(id="start_order")
def start_order(context):
    publish_event("OrderStarted", context.params)

@choreographed_workflow.event_handler("InventoryReserved")
def on_inventory_reserved(event):
    publish_event("PaymentRequested", event.data)

@choreographed_workflow.event_handler("PaymentCompleted")
def on_payment_completed(event):
    publish_event("ShipmentRequested", event.data)
```

## MapReduce Pattern

```python
from deerflow import Workflow, MapReduce

workflow = Workflow(name="distributed_analysis")

@workflow.map_reduce(
    id="analyze_logs",
    partitions=100,
    reduce_parallelism=10
)
class LogAnalysis(MapReduce):
    def partition(self, context):
        """Partition input data."""
        log_files = list_log_files(context.params["date"])
        return [{"file": f} for f in log_files]

    def map(self, partition, context):
        """Process each partition."""
        file_path = partition["file"]
        counts = {}

        for line in read_log_file(file_path):
            error_type = extract_error_type(line)
            if error_type:
                counts[error_type] = counts.get(error_type, 0) + 1

        return counts

    def reduce(self, results, context):
        """Combine all results."""
        combined = {}
        for result in results:
            for error_type, count in result.items():
                combined[error_type] = combined.get(error_type, 0) + count

        return {
            "total_errors": sum(combined.values()),
            "by_type": combined
        }
```

## Pipeline Patterns

### Fan-Out / Fan-In

```python
from deerflow import Workflow, parallel, gather

workflow = Workflow(name="parallel_processing")

@workflow.task(id="split")
def split_data(context):
    data = load_large_dataset()
    chunks = split_into_chunks(data, num_chunks=10)
    return {"chunks": chunks}

@workflow.parallel_tasks(id="process_chunks", depends_on=["split"])
def process_chunk(chunk, context):
    """This runs in parallel for each chunk."""
    return process_data(chunk)

@workflow.task(id="merge", depends_on=["process_chunks"])
def merge_results(context):
    """Gather and merge all parallel results."""
    results = context.parallel_results["process_chunks"]
    return merge_datasets(results)
```

### Pipeline with Backpressure

```python
from deerflow import Workflow, Pipeline, Backpressure

workflow = Workflow(name="streaming_pipeline")

@workflow.pipeline(
    backpressure=Backpressure(
        max_buffer_size=1000,
        strategy="block"  # block, drop, or sample
    )
)
class DataPipeline(Pipeline):
    @stage(parallelism=5)
    def extract(self, item):
        return fetch_record(item)

    @stage(parallelism=10)
    def transform(self, record):
        return transform_record(record)

    @stage(parallelism=3, batch_size=100)
    def load(self, batch):
        return bulk_insert(batch)
```

## State Machine Workflows

```python
from deerflow import Workflow, StateMachine, State, Transition

workflow = Workflow(name="order_state_machine")

@workflow.state_machine
class OrderStateMachine(StateMachine):
    # Define states
    pending = State(initial=True)
    confirmed = State()
    processing = State()
    shipped = State()
    delivered = State(final=True)
    cancelled = State(final=True)

    # Define transitions
    confirm = Transition(source=pending, target=confirmed)
    start_processing = Transition(source=confirmed, target=processing)
    ship = Transition(source=processing, target=shipped)
    deliver = Transition(source=shipped, target=delivered)
    cancel = Transition(source=[pending, confirmed], target=cancelled)

    # Transition handlers
    @on_transition(confirm)
    def on_confirm(self, context):
        send_confirmation_email(context.order)

    @on_transition(ship)
    def on_ship(self, context):
        notify_customer(context.order, "shipped")

    @on_transition(cancel)
    def on_cancel(self, context):
        refund_payment(context.order)
```

## Summary

In this chapter, you've learned:

- **Dynamic Workflows**: Runtime task generation
- **Sub-Workflows**: Nested and composed workflows
- **Event-Driven**: Triggers and event sourcing
- **Saga Pattern**: Distributed transactions
- **MapReduce**: Parallel data processing
- **State Machines**: Complex state transitions

## Key Takeaways

1. **Dynamic for Flexibility**: Generate tasks at runtime
2. **Compose for Reuse**: Build complex from simple workflows
3. **Events for Decoupling**: Loose coupling between components
4. **Sagas for Consistency**: Handle distributed transactions
5. **Patterns for Scale**: MapReduce for big data

## Tutorial Complete

Congratulations! You've completed the Deer Flow tutorial. You now have the knowledge to:

- Design and implement complex distributed workflows
- Handle failures with retries, fallbacks, and sagas
- Scale workflows across clusters
- Monitor and observe workflow execution
- Apply advanced orchestration patterns

## Further Resources

- [Deer Flow Documentation](https://github.com/bytedance/deer-flow/tree/main/docs)
- [GitHub Repository](https://github.com/bytedance/deer-flow)
- [Example Workflows](https://github.com/bytedance/deer-flow/tree/main/examples)

---

*Generated for [Awesome Code Docs](https://github.com/johnxie/awesome-code-docs)*
