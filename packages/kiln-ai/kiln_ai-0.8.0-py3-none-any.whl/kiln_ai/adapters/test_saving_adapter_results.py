from unittest.mock import patch

import pytest

from kiln_ai.adapters.base_adapter import AdapterInfo, BaseAdapter, RunOutput
from kiln_ai.datamodel import (
    DataSource,
    DataSourceType,
    Project,
    Task,
)
from kiln_ai.utils.config import Config


class MockAdapter(BaseAdapter):
    async def _run(self, input: dict | str) -> dict | str:
        return RunOutput(output="Test output", intermediate_outputs=None)

    def adapter_info(self) -> AdapterInfo:
        return AdapterInfo(
            adapter_name="mock_adapter",
            model_name="mock_model",
            model_provider="mock_provider",
            prompt_builder_name="mock_prompt_builder",
        )


@pytest.fixture
def test_task(tmp_path):
    project = Project(name="test_project", path=tmp_path / "test_project.kiln")
    project.save_to_file()
    task = Task(
        parent=project,
        name="test_task",
        instruction="Task instruction",
    )
    task.save_to_file()
    return task


def test_save_run_isolation(test_task):
    adapter = MockAdapter(test_task)
    input_data = "Test input"
    output_data = "Test output"
    run_output = RunOutput(
        output=output_data,
        intermediate_outputs={"chain_of_thought": "Test chain of thought"},
    )

    task_run = adapter.generate_run(
        input=input_data, input_source=None, run_output=run_output
    )
    task_run.save_to_file()

    # Check that the task input was saved correctly
    assert task_run.parent == test_task
    assert task_run.input == input_data
    assert task_run.input_source.type == DataSourceType.human
    assert task_run.intermediate_outputs == {
        "chain_of_thought": "Test chain of thought"
    }
    created_by = Config.shared().user_id
    if created_by and created_by != "":
        assert task_run.input_source.properties["created_by"] == created_by
    else:
        assert "created_by" not in task_run.input_source.properties

    # Check that the task output was saved correctly
    saved_output = task_run.output
    assert saved_output.output == output_data
    assert saved_output.source.type == DataSourceType.synthetic
    assert saved_output.rating is None

    # Verify that the data can be read back from disk
    reloaded_task = Task.load_from_file(test_task.path)
    reloaded_runs = reloaded_task.runs()
    assert len(reloaded_runs) == 1
    reloaded_run = reloaded_runs[0]
    assert reloaded_run.input == input_data
    assert reloaded_run.input_source.type == DataSourceType.human
    reloaded_output = reloaded_run.output

    reloaded_output = reloaded_run.output
    assert reloaded_output.output == output_data
    assert reloaded_output.source.type == DataSourceType.synthetic
    assert reloaded_output.rating is None
    assert reloaded_output.source.properties["adapter_name"] == "mock_adapter"
    assert reloaded_output.source.properties["model_name"] == "mock_model"
    assert reloaded_output.source.properties["model_provider"] == "mock_provider"
    assert (
        reloaded_output.source.properties["prompt_builder_name"]
        == "mock_prompt_builder"
    )

    # Run again, with same input and different output. Should create a new TaskRun.
    different_run_output = RunOutput(
        output="Different output", intermediate_outputs=None
    )
    task_output = adapter.generate_run(input_data, None, different_run_output)
    task_output.save_to_file()
    assert len(test_task.runs()) == 2
    assert "Different output" in set(run.output.output for run in test_task.runs())

    # run again with same input and same output. Should not create a new TaskRun.
    task_output = adapter.generate_run(input_data, None, run_output)
    task_output.save_to_file()
    assert len(test_task.runs()) == 2
    assert "Different output" in set(run.output.output for run in test_task.runs())
    assert output_data in set(run.output.output for run in test_task.runs())

    # run again with input of different type. Should create a new TaskRun and TaskOutput.
    task_output = adapter.generate_run(
        input_data,
        DataSource(
            type=DataSourceType.synthetic,
            properties={
                "model_name": "mock_model",
                "model_provider": "mock_provider",
                "prompt_builder_name": "mock_prompt_builder",
                "adapter_name": "mock_adapter",
            },
        ),
        run_output,
    )
    task_output.save_to_file()
    assert len(test_task.runs()) == 3
    assert task_output.input == input_data
    assert task_output.input_source.type == DataSourceType.synthetic
    assert "Different output" in set(run.output.output for run in test_task.runs())
    assert output_data in set(run.output.output for run in test_task.runs())


@pytest.mark.asyncio
async def test_autosave_false(test_task):
    with patch("kiln_ai.utils.config.Config.shared") as mock_shared:
        mock_config = mock_shared.return_value
        mock_config.autosave_runs = False
        mock_config.user_id = "test_user"

        adapter = MockAdapter(test_task)
        input_data = "Test input"

        run = await adapter.invoke(input_data)

        # Check that no runs were saved
        assert len(test_task.runs()) == 0

        # Check that the run ID is not set
        assert run.id is None


@pytest.mark.asyncio
async def test_autosave_true(test_task):
    with patch("kiln_ai.utils.config.Config.shared") as mock_shared:
        mock_config = mock_shared.return_value
        mock_config.autosave_runs = True
        mock_config.user_id = "test_user"

        adapter = MockAdapter(test_task)
        input_data = "Test input"

        run = await adapter.invoke(input_data)

        # Check that the run ID is set
        assert run.id is not None

        # Check that an task input was saved
        task_runs = test_task.runs()
        assert len(task_runs) == 1
        assert task_runs[0].input == input_data
        assert task_runs[0].input_source.type == DataSourceType.human

        output = task_runs[0].output
        assert output.output == "Test output"
        assert output.source.type == DataSourceType.synthetic
        assert output.source.properties["adapter_name"] == "mock_adapter"
        assert output.source.properties["model_name"] == "mock_model"
        assert output.source.properties["model_provider"] == "mock_provider"
        assert output.source.properties["prompt_builder_name"] == "mock_prompt_builder"
