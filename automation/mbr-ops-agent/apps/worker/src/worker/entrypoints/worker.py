"""MBR Records worker entrypoint.

Discovers every workflow in the workflows package and serves them.
The managed deployment injects the service-account token; the SDK reads it.
"""
import asyncio

import mistralai.workflows as workflows


async def main() -> None:
    workflow_classes = workflows.discover_all_workflows_in_package("worker.workflows")
    await workflows.run_worker(workflow_classes)


if __name__ == "__main__":
    asyncio.run(main())
