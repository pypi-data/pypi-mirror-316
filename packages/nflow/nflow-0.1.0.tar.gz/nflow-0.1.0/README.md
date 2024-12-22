# nFlow Client SDK

The `nFlow Client SDK` is a Python package designed for creating, managing, and executing media processing pipelines. It provides an easy-to-use interface for defining pipeline workflows, managing resources, and scheduling jobs.

---

## Features
- Define pipelines with modular operators.
- Manage input and output resources.
- Schedule pipeline jobs with cron-like triggers.
- Track progress for long-running tasks (e.g., uploads, downloads, execution).
- Designed for cloud-native environments.

---

## Installation

To install the `nflow-client-sdk`, use `pip`:

```bash
pip install nflow-client-sdk

```

## Quick Start

Here’s an example of using the SDK to define and execute a pipeline:
```python
import asyncio
from nflow import Resource, Operator, Pipeline, Job, Trigger

# Progress callback for resources
def show_progress(progress):
    print(f"Progress: {progress:.2f}%")

async def main():
    # Step 1: Create resources
    input_resource = Resource("input_video", "collection_name", "file", "mp4")
    output_resource = Resource("output_stream", "collection_name", "live", "rtsp://localhost:8554/test")

    # Step 2: Upload input resource
    await input_resource.upload_async("/path/to/input", progress_callback=show_progress)

    # Step 3: Create operators
    loader = Operator("MP4FileLoaderOp", params={"resource_id": input_resource.id})
    brighten_op1 = Operator("BrightenConvOp", params={"brightness": 1.8})
    brighten_op2 = Operator("BrightenConvOp", params={"brightness": 1.8})
    sender = Operator("RTSPStreamSenderOp", params={"resource_id": output_resource.id})

    # Step 4: Create and link pipeline
    pipeline = Pipeline("my_pipeline")
    pipeline.link(loader, "video-out", brighten_op1, "video-in")
    pipeline.link(brighten_op1, "video-out", brighten_op2, "video-in")
    pipeline.link(brighten_op2, "video-out", sender, "video-in")
    pipeline.link(loader, "audio-out", sender, "audio-in")

    pipeline_id = pipeline.register()

    # Step 5: Schedule a job
    trigger = Trigger(cron="*/5 * * * *")
    job = Job(pipeline_id, trigger)
    job_id = job.start()
    print(f"Job '{job_id}' has been scheduled with trigger: {trigger.cron}")

    # Step 6: Run the job and wait for completion
    await job.run()
    print("Job completed!")

    # Step 7: Download the output resource
    await output_resource.download_async("/path/to/output", progress_callback=show_progress)
    print("Output resource downloaded!")

# Run the workflow
asyncio.run(main())
```

## Operators
Operators are modular processing units that perform specific tasks in a pipeline. They encapsulate their behavior and parameters for easy integration into the pipeline workflow.

### Available Operators:
- **`MP4FileLoaderOp`**:
  - **Purpose**: Loads an MP4 file as input to the pipeline.
  - **Parameters**:
    - `resource_id` (str): The ID of the resource to load.

- **`BrightenConvOp`**:
  - **Purpose**: Adjusts the brightness of video frames.
  - **Parameters**:
    - `brightness` (float): Brightness adjustment factor (e.g., `1.8`).

- **`RTSPStreamSenderOp`**:
  - **Purpose**: Sends the output of the pipeline as an RTSP stream.
  - **Parameters**:
    - `resource_id` (str): The ID of the output resource.

---

## Pipelines
Pipelines define the logical flow of operations by linking operators. A pipeline manages how data flows from one operator to the next.

### Creating a Pipeline
1. Instantiate a `Pipeline` object:
   ```python
   pipeline = Pipeline("my_pipeline")
   ```
2. Add operators to the pipeline using the link() method:
    ```python
    pipeline.link(source_operator, "output_pad_name", target_operator, "input_pad_name")
    ```
3. Register the pipeline to prepare it for execution: 
    ```python
    pipeline_id = pipeline.register()
    ```

## Jobs and Triggers
Jobs are responsible for executing pipelines, and triggers define when or how jobs are executed.

### Scheduling a Job
1. Define a trigger with a cron-like schedule:
   ```python
   trigger = Trigger(cron="*/5 * * * *")  # Every 5 minutes
   ```
2. Create a job and associate it with a pipeline:
    ```python
    job = Job(pipeline_id, trigger)
    ```
3. Start the job: 
    ```python
    job_id = job.start()
    ```
4. Optionally, wait for the job to execute:
    ```python
    await job.run()
    ```

# License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

---

# Contributing

Contributions are welcome! Please open an issue or submit a pull request.

---

# Contact

For questions or support, please contact us at `support@example.com`.
