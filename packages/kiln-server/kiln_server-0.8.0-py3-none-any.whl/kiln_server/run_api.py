from asyncio import Lock
from datetime import datetime
from typing import Any, Dict

from fastapi import FastAPI, HTTPException
from kiln_ai.adapters.adapter_registry import adapter_for_task
from kiln_ai.adapters.prompt_builders import prompt_builder_from_ui_name
from kiln_ai.datamodel import Task, TaskOutputRating, TaskOutputRatingType, TaskRun
from kiln_ai.datamodel.basemodel import ID_TYPE
from pydantic import BaseModel, ConfigDict

from kiln_server.task_api import task_from_id

# Lock to prevent overwriting via concurrent updates. We use a load/update/write pattern that is not atomic.
update_run_lock = Lock()


def deep_update(
    source: Dict[str, Any] | None, update: Dict[str, Any | None]
) -> Dict[str, Any]:
    if source is None:
        return {k: v for k, v in update.items() if v is not None}
    for key, value in update.items():
        if value is None:
            source.pop(key, None)
        elif isinstance(value, dict):
            if key not in source or not isinstance(source[key], dict):
                source[key] = {}
            source[key] = deep_update(source[key], value)
        else:
            source[key] = value
    return {k: v for k, v in source.items() if v is not None}


class RunTaskRequest(BaseModel):
    model_name: str
    provider: str
    plaintext_input: str | None = None
    structured_input: Dict[str, Any] | None = None
    ui_prompt_method: str | None = None
    tags: list[str] | None = None

    # Allows use of the model_name field (usually pydantic will reserve model_*)
    model_config = ConfigDict(protected_namespaces=())


class RunSummary(BaseModel):
    id: ID_TYPE
    rating: TaskOutputRating | None = None
    created_at: datetime
    input_preview: str | None = None
    output_preview: str | None = None
    repair_state: str | None = None
    model_name: str | None = None
    input_source: str | None = None
    tags: list[str] | None = None

    @classmethod
    def format_preview(cls, text: str | None, max_length: int = 100) -> str | None:
        if text is None:
            return None
        if len(text) > max_length:
            return text[:max_length] + "…"
        return text

    @classmethod
    def repair_status_display_name(cls, run: TaskRun) -> str:
        if run.repair_instructions:
            return "Repaired"
        elif run.output and not run.output.rating:
            return "Rating needed"
        elif not run.output or not run.output.output:
            return "No output"
        elif (
            run.output.rating
            and run.output.rating.value == 5.0
            and run.output.rating.type == TaskOutputRatingType.five_star
        ):
            return "No repair needed"
        elif (
            run.output.rating
            and run.output.rating.type != TaskOutputRatingType.five_star
        ):
            return "Unknown"
        elif run.output.output:
            return "Repair needed"
        return "Unknown"

    @classmethod
    def from_run(cls, run: TaskRun) -> "RunSummary":
        model_name = (
            run.output.source.properties.get("model_name")
            if run.output and run.output.source and run.output.source.properties
            else None
        )
        if not isinstance(model_name, str):
            model_name = None
        output = run.output.output if run.output and run.output.output else None

        return RunSummary(
            id=run.id,
            rating=run.output.rating,
            tags=run.tags,
            input_preview=RunSummary.format_preview(run.input),
            output_preview=RunSummary.format_preview(output),
            created_at=run.created_at,
            repair_state=RunSummary.repair_status_display_name(run),
            model_name=model_name,
            input_source=run.input_source.type if run.input_source else None,
        )


def run_from_id(project_id: str, task_id: str, run_id: str) -> TaskRun:
    task, run = task_and_run_from_id(project_id, task_id, run_id)
    return run


def task_and_run_from_id(
    project_id: str, task_id: str, run_id: str
) -> tuple[Task, TaskRun]:
    task = task_from_id(project_id, task_id)
    run = TaskRun.from_id_and_parent_path(run_id, task.path)
    if run:
        return task, run

    raise HTTPException(
        status_code=404,
        detail=f"Run not found. ID: {run_id}",
    )


def connect_run_api(app: FastAPI):
    @app.get("/api/projects/{project_id}/tasks/{task_id}/runs/{run_id}")
    async def get_run(project_id: str, task_id: str, run_id: str) -> TaskRun:
        return run_from_id(project_id, task_id, run_id)

    @app.delete("/api/projects/{project_id}/tasks/{task_id}/runs/{run_id}")
    async def delete_run(project_id: str, task_id: str, run_id: str):
        run = run_from_id(project_id, task_id, run_id)
        run.delete()

    @app.get("/api/projects/{project_id}/tasks/{task_id}/runs")
    async def get_runs(project_id: str, task_id: str) -> list[TaskRun]:
        task = task_from_id(project_id, task_id)
        return list(task.runs())

    @app.get("/api/projects/{project_id}/tasks/{task_id}/runs_summaries")
    async def get_runs_summary(project_id: str, task_id: str) -> list[RunSummary]:
        task = task_from_id(project_id, task_id)
        runs = task.runs()
        run_summaries: list[RunSummary] = []
        for run in runs:
            summary = RunSummary.from_run(run)
            run_summaries.append(summary)
        return run_summaries

    @app.post("/api/projects/{project_id}/tasks/{task_id}/run")
    async def run_task(
        project_id: str, task_id: str, request: RunTaskRequest
    ) -> TaskRun:
        task = task_from_id(project_id, task_id)

        prompt_builder_class = prompt_builder_from_ui_name(
            request.ui_prompt_method or "basic"
        )
        if prompt_builder_class is None:
            raise HTTPException(
                status_code=400,
                detail=f"Unknown prompt method: {request.ui_prompt_method}",
            )
        prompt_builder = prompt_builder_class(task)
        adapter = adapter_for_task(
            task,
            model_name=request.model_name,
            provider=request.provider,
            prompt_builder=prompt_builder,
            tags=request.tags,
        )

        input = request.plaintext_input
        if task.input_schema() is not None:
            input = request.structured_input

        if input is None:
            raise HTTPException(
                status_code=400,
                detail="No input provided. Ensure your provided the proper format (plaintext or structured).",
            )

        return await adapter.invoke(input)

    @app.patch("/api/projects/{project_id}/tasks/{task_id}/runs/{run_id}")
    async def update_run(
        project_id: str, task_id: str, run_id: str, run_data: Dict[str, Any]
    ) -> TaskRun:
        return await update_run_util(project_id, task_id, run_id, run_data)


async def update_run_util(
    project_id: str, task_id: str, run_id: str, run_data: Dict[str, Any]
) -> TaskRun:
    # Lock to prevent overwriting concurrent updates
    async with update_run_lock:
        task = task_from_id(project_id, task_id)

        run = TaskRun.from_id_and_parent_path(run_id, task.path)
        if run is None:
            raise HTTPException(
                status_code=404,
                detail=f"Run not found. ID: {run_id}",
            )

        # Update and save
        old_run_dumped = run.model_dump()
        merged = deep_update(old_run_dumped, run_data)
        updated_run = TaskRun.model_validate(merged)
        updated_run.path = run.path
        updated_run.save_to_file()
        return updated_run
