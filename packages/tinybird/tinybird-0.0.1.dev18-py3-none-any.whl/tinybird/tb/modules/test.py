# This is a command file for our CLI. Please keep it clean.
#
# - If it makes sense and only when strictly necessary, you can create utility functions in this file.
# - But please, **do not** interleave utility functions and command definitions.

import difflib
import glob
import os
from pathlib import Path
from typing import Iterable, List, Optional, Tuple

import click
import yaml

from tinybird.feedback_manager import FeedbackManager
from tinybird.tb.modules.cli import cli
from tinybird.tb.modules.common import coro
from tinybird.tb.modules.config import CLIConfig
from tinybird.tb.modules.exceptions import CLIException
from tinybird.tb.modules.llm import LLM, TestExpectation
from tinybird.tb.modules.local_common import get_tinybird_local_client

yaml.SafeDumper.org_represent_str = yaml.SafeDumper.represent_str


def repr_str(dumper, data):
    if "\n" in data:
        return dumper.represent_scalar("tag:yaml.org,2002:str", data, style="|")
    return dumper.org_represent_str(data)


yaml.add_representer(str, repr_str, Dumper=yaml.SafeDumper)


def generate_test_file(pipe_name: str, tests: List[TestExpectation], folder: Optional[str], mode: str = "w"):
    base = Path("tests")
    if folder:
        base = Path(folder) / base

    base.mkdir(parents=True, exist_ok=True)

    yaml_str = yaml.safe_dump(tests, sort_keys=False)
    formatted_yaml = yaml_str.replace("- name:", "\n- name:")

    path = base / f"{pipe_name}.yaml"
    with open(path, mode) as f:
        f.write(formatted_yaml)


@cli.group()
@click.pass_context
def test(ctx: click.Context) -> None:
    """Test commands."""


@test.command(
    name="create",
    help="Create a test for an existing endpoint",
)
@click.argument("pipe", type=str)
@click.option(
    "--folder",
    default=".",
    type=click.Path(exists=True, file_okay=False),
    help="Folder where datafiles will be placed",
)
@click.option("--prompt", type=str, default=None, help="Prompt to be used to create the test")
@click.pass_context
@coro
async def test_create(ctx: click.Context, pipe: str, prompt: Optional[str], folder: Optional[str]) -> None:
    """
    Create a test for an existing endpoint
    """

    try:
        pipe_path = Path(pipe)
        pipe_name = pipe
        if pipe_path.suffix == ".pipe":
            pipe_name = pipe_path.stem
        else:
            pipe_path = Path("endpoints", f"{pipe}.pipe")
            if not pipe_path.exists():
                pipe_path = Path("pipes", f"{pipe}.pipe")

        click.echo(FeedbackManager.gray(message=f"\nCreating tests for {pipe_name} endpoint..."))
        pipe_path = Path(folder) / pipe_path
        pipe_content = pipe_path.read_text()

        client = await get_tinybird_local_client(os.path.abspath(folder))
        pipe_nodes = await client._req(f"/v0/pipes/{pipe_name}")
        pipe_params = set([param["name"] for node in pipe_nodes["nodes"] for param in node["params"]])

        llm_config = CLIConfig.get_llm_config()
        llm = LLM(client=client, api_key=llm_config["api_key"])

        test_expectations = await llm.create_test_commands(
            pipe_content=pipe_content, pipe_params=pipe_params, context=prompt
        )
        valid_test_expectations = []
        for test in test_expectations.tests:
            valid_test = test.model_dump()
            test_params = (
                valid_test["parameters"] if valid_test["parameters"].startswith("?") else f"?{valid_test['parameters']}"
            )
            response = ""
            try:
                response = await client._req(f"/v0/pipes/{pipe_name}.ndjson{test_params}")
            except Exception:
                valid_test["expected_http_status"] = 500

            valid_test["expected_result"] = response
            valid_test_expectations.append(valid_test)
        if valid_test_expectations:
            generate_test_file(pipe_name, valid_test_expectations, folder, mode="a")
            click.echo(FeedbackManager.info(message=f"✓ /tests/{pipe_name}.yaml"))
        click.echo(FeedbackManager.success(message="✓ Done!\n"))
    except Exception as e:
        raise CLIException(FeedbackManager.error_exception(error=e))


@test.command(
    name="update",
    help="Update the test expectations for a file or a test.",
)
@click.argument("pipe", type=str)
@click.option(
    "--folder",
    default=".",
    type=click.Path(exists=True, file_okay=False),
    help="Folder where datafiles will be placed",
)
@click.pass_context
@coro
async def test_update(ctx: click.Context, pipe: str, folder: Optional[str]) -> None:
    client = await get_tinybird_local_client(os.path.abspath(folder))

    pipe_tests_path = Path(pipe)
    pipe_name = pipe
    if pipe_tests_path.suffix == ".yaml":
        pipe_name = pipe_tests_path.stem
    else:
        pipe_tests_path = Path("tests", f"{pipe}.yaml")

    click.echo(FeedbackManager.gray(message=f"\nUpdating tests expectations for {pipe_name} endpoint..."))
    pipe_tests_path = Path(folder) / pipe_tests_path
    pipe_tests_content = yaml.safe_load(pipe_tests_path.read_text())
    for test in pipe_tests_content:
        test_params = test["parameters"] if test["parameters"].startswith("?") else f"?{test['parameters']}"
        response = ""
        try:
            response = await client._req(f"/v0/pipes/{pipe_name}.ndjson{test_params}")
        except Exception:
            test["expected_http_status"] = 500
        else:
            if "expected_http_status" in test:
                del test["expected_http_status"]

        test["expected_result"] = response

    generate_test_file(pipe_name, pipe_tests_content, folder)
    click.echo(FeedbackManager.info(message=f"✓ /tests/{pipe_name}.yaml"))
    click.echo(FeedbackManager.success(message="✓ Done!\n"))


@test.command(
    name="run",
    help="Run the test suite, a file, or a test.",
)
@click.argument("file", nargs=-1)
@click.option(
    "--folder",
    default=".",
    type=click.Path(exists=True, file_okay=False),
    help="Folder where tests will be placed",
)
@click.pass_context
@coro
async def test_run(ctx: click.Context, file: Tuple[str, ...], folder: Optional[str]) -> None:
    client = await get_tinybird_local_client(os.path.abspath(folder))
    file_list: Iterable[str] = file if len(file) > 0 else glob.glob("./tests/**/*.y*ml", recursive=True)

    async def run_test(test_file):
        test_file_path = Path(test_file)
        test_file_content = yaml.safe_load(test_file_path.read_text())
        for test in test_file_content:
            try:
                test_params = test["parameters"] if test["parameters"].startswith("?") else f"?{test['parameters']}"
                response = ""
                try:
                    response = await client._req(f"/v0/pipes/{test_file_path.stem}.ndjson{test_params}")
                except Exception:
                    if "expected_http_status" not in test:
                        raise Exception("Expected to not fail but got an error")
                    if test["expected_http_status"] != 500:
                        raise Exception(f"Expected {test['expected_http_status']} but got another status")

                if test["expected_result"] != response:
                    diff = difflib.ndiff(
                        test["expected_result"].splitlines(keepends=True), response.splitlines(keepends=True)
                    )
                    printable_diff = "".join(diff)
                    raise Exception(
                        f"\nExpected: \n{test['expected_result']}\nGot: \n{response}\nDiff: \n{printable_diff}"
                    )
                click.echo(FeedbackManager.success(message=f"✓ {test_file_path.name} - {test['name']}"))
            except Exception as e:
                click.echo(FeedbackManager.error(message=f"✗ {test_file_path.name} - {test['name']}"))
                click.echo(FeedbackManager.error(message=f"Output and expected output are different: \n{e}"))

    for test_file in file_list:
        await run_test(test_file)
