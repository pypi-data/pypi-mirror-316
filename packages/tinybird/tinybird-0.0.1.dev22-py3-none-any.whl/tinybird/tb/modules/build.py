import asyncio
import os
import threading
import time
from pathlib import Path
from typing import List

import click

import tinybird.context as context
from tinybird.client import TinyB
from tinybird.config import FeatureFlags
from tinybird.tb.modules.cli import cli
from tinybird.tb.modules.common import push_data
from tinybird.tb.modules.datafile.build import folder_build
from tinybird.tb.modules.datafile.common import get_project_filenames, get_project_fixtures, has_internal_datafiles
from tinybird.tb.modules.datafile.exceptions import ParseException
from tinybird.tb.modules.datafile.fixture import build_fixture_name, get_fixture_dir
from tinybird.tb.modules.datafile.parse_datasource import parse_datasource
from tinybird.tb.modules.datafile.parse_pipe import parse_pipe
from tinybird.tb.modules.feedback_manager import FeedbackManager
from tinybird.tb.modules.local_common import get_tinybird_local_client
from tinybird.tb.modules.shell import Shell, print_table_formatted
from tinybird.tb.modules.watch import watch_files


@cli.command()
@click.option(
    "--folder",
    default=".",
    help="Folder from where to execute the command. By default the current folder",
    hidden=True,
    type=click.types.STRING,
)
@click.option(
    "--watch",
    is_flag=True,
    help="Watch for changes in the files and re-check them.",
)
def build(
    folder: str,
    watch: bool,
) -> None:
    """
    Watch for changes in the files and re-check them.
    """
    ignore_sql_errors = FeatureFlags.ignore_sql_errors()
    context.disable_template_security_validation.set(True)
    is_internal = has_internal_datafiles(folder)
    folder_path = os.path.abspath(folder)
    tb_client = asyncio.run(get_tinybird_local_client(folder_path))

    def check_filenames(filenames: List[str]):
        parser_matrix = {".pipe": parse_pipe, ".datasource": parse_datasource}
        incl_suffix = ".incl"

        for filename in filenames:
            if os.path.isdir(filename):
                check_filenames(filenames=get_project_filenames(filename))

            file_suffix = Path(filename).suffix
            if file_suffix == incl_suffix:
                continue

            parser = parser_matrix.get(file_suffix)
            if not parser:
                raise ParseException(FeedbackManager.error_unsupported_datafile(extension=file_suffix))

            parser(filename)

    async def process(filenames: List[str], watch: bool = False):
        datafiles = [f for f in filenames if f.endswith(".datasource") or f.endswith(".pipe")]
        if len(datafiles) > 0:
            check_filenames(filenames=datafiles)
            await folder_build(
                tb_client,
                filenames=datafiles,
                ignore_sql_errors=ignore_sql_errors,
                is_internal=is_internal,
                watch=watch,
            )
        if len(filenames) > 0:
            filename = filenames[0]
            if filename.endswith(".ndjson"):
                fixture_path = Path(filename)
                name = "_".join(fixture_path.stem.split("_")[:-1])
                ds_path = Path(folder) / "datasources" / f"{name}.datasource"
                if ds_path.exists():
                    await append_datasource(tb_client, name, str(fixture_path), silent=True)

            if watch:
                if filename.endswith(".datasource"):
                    ds_path = Path(filename)
                    name = build_fixture_name(filename, ds_path.stem, ds_path.read_text())
                    fixture_path = get_fixture_dir() / f"{name}.ndjson"
                    if fixture_path.exists():
                        await append_datasource(tb_client, ds_path.stem, str(fixture_path), silent=True)
                if not filename.endswith(".ndjson"):
                    await build_and_print_resource(tb_client, filename)

    datafiles = get_project_filenames(folder)
    fixtures = get_project_fixtures(folder)
    filenames = datafiles + fixtures

    async def build_once(filenames: List[str]):
        ok = False
        try:
            click.echo("⚡ Building project...\n")
            time_start = time.time()
            await process(filenames=filenames, watch=False)
            time_end = time.time()
            elapsed_time = time_end - time_start
            for filename in filenames:
                if filename.endswith(".datasource"):
                    ds_path = Path(filename)
                    name = build_fixture_name(filename, ds_path.stem, ds_path.read_text())
                    fixture_path = get_fixture_dir() / f"{name}.ndjson"
                    if fixture_path.exists():
                        await append_datasource(tb_client, ds_path.stem, str(fixture_path), silent=True)
            click.echo(FeedbackManager.success(message=f"\n✓ Build completed in {elapsed_time:.1f}s\n"))
            ok = True
        except Exception as e:
            click.echo(FeedbackManager.error(message=str(e)))
            ok = False
        return ok

    build_ok = asyncio.run(build_once(filenames))

    if watch:
        paths = [Path(f) for f in get_project_filenames(folder, with_vendor=True)]

        def is_vendor(f: Path) -> bool:
            return f.parts[0] == "vendor"

        def get_vendor_workspace(f: Path) -> str:
            return f.parts[1]

        def is_endpoint(f: Path) -> bool:
            return f.suffix == ".pipe" and not is_vendor(f) and f.parts[0] == "endpoints"

        def is_pipe(f: Path) -> bool:
            return f.suffix == ".pipe" and not is_vendor(f)

        datasource_paths = [f for f in paths if f.suffix == ".datasource"]
        datasources = [f.stem for f in datasource_paths if not is_vendor(f)]
        shared_datasources = [f"{get_vendor_workspace(f)}.{f.stem}" for f in datasource_paths if is_vendor(f)]
        pipes = [f.stem for f in paths if is_pipe(f) and not is_endpoint(f)]
        endpoints = [f.stem for f in paths if is_endpoint(f)]
        shell = Shell(
            folder=folder,
            client=tb_client,
            datasources=datasources,
            shared_datasources=shared_datasources,
            pipes=pipes,
            endpoints=endpoints,
        )
        click.echo(FeedbackManager.highlight(message="◎ Watching for changes..."))
        watcher_thread = threading.Thread(
            target=watch_files, args=(filenames, process, shell, folder, build_ok), daemon=True
        )
        watcher_thread.start()
        shell.run()


async def build_and_print_resource(tb_client: TinyB, filename: str):
    resource_path = Path(filename)
    name = resource_path.stem
    pipeline = name if filename.endswith(".pipe") else None
    res = await tb_client.query(f"SELECT * FROM {name} FORMAT JSON", pipeline=pipeline)
    print_table_formatted(res, name)


async def append_datasource(
    tb_client: TinyB,
    datasource_name: str,
    url: str,
    silent: bool = False,
):
    await push_data(
        tb_client,
        datasource_name,
        url,
        mode="append",
        concurrency=1,
        silent=silent,
    )
