import logging
import os
from pathlib import Path

import click

from tinybird.tb.modules.cli import cli
from tinybird.tb.modules.common import CLIException, check_user_token, coro
from tinybird.tb.modules.config import CLIConfig
from tinybird.tb.modules.datafile.fixture import build_fixture_name, persist_fixture
from tinybird.tb.modules.feedback_manager import FeedbackManager
from tinybird.tb.modules.llm import LLM
from tinybird.tb.modules.local_common import get_tinybird_local_client


@cli.command()
@click.argument("datasource", type=str)
@click.option("--rows", type=int, default=10, help="Number of events to send")
@click.option("--prompt", type=str, default="", help="Extra context to use for data generation")
@click.option("--folder", type=str, default=".", help="Folder where datafiles will be placed")
@click.pass_context
@coro
async def mock(ctx: click.Context, datasource: str, rows: int, prompt: str, folder: str) -> None:
    """Load sample data into a Data Source.

    Args:
        ctx: Click context object
        datasource_file: Path to the datasource file to load sample data into
    """

    try:
        datasource_path = Path(datasource)
        datasource_name = datasource
        if datasource_path.suffix == ".datasource":
            datasource_name = datasource_path.stem
        else:
            datasource_path = Path("datasources", f"{datasource}.datasource")
        datasource_path = Path(folder) / datasource_path

        prompt_path = Path(folder) / "fixtures" / f"{datasource_name}.prompt"
        if not prompt:
            # load the prompt from the fixture.prompt file if it exists
            if prompt_path.exists():
                prompt = prompt_path.read_text()
        else:
            click.echo(FeedbackManager.gray(message=f"Overriding prompt for {datasource_name}..."))
            prompt_path.write_text(prompt)

        click.echo(FeedbackManager.gray(message=f"Creating fixture for {datasource_name}..."))
        datasource_content = datasource_path.read_text()
        config = CLIConfig.get_project_config()
        user_client = config.get_client()
        user_token = config.get_user_token()

        try:
            if not user_token:
                raise CLIException("No user token found")
            await check_user_token(ctx, token=user_token)
        except Exception:
            click.echo(FeedbackManager.error(message="This action requires authentication. Run 'tb login' first."))
            return

        llm = LLM(user_token=user_token, client=user_client)
        tb_client = await get_tinybird_local_client(os.path.abspath(folder))
        sql = await llm.generate_sql_sample_data(datasource_content, rows=rows, prompt=prompt)
        if os.environ.get("TB_DEBUG", "") != "":
            logging.debug(sql)
        result = await tb_client.query(f"{sql} FORMAT JSON")
        data = result.get("data", [])[:rows]
        fixture_name = build_fixture_name(datasource_path.absolute().as_posix(), datasource_name, datasource_content)
        persist_fixture(fixture_name, data)
        click.echo(FeedbackManager.success(message="✓ Done!"))

    except Exception as e:
        raise CLIException(FeedbackManager.error_exception(error=e))
