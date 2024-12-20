import asyncio
import time
from typing import Any, Callable, List

import click
from watchdog.events import FileSystemEventHandler
from watchdog.observers import Observer

from tinybird.tb.modules.feedback_manager import FeedbackManager
from tinybird.tb.modules.shell import Shell


class FileChangeHandler(FileSystemEventHandler):
    def __init__(self, filenames: List[str], process: Callable[[List[str]], None], build_ok: bool):
        self.filenames = filenames
        self.process = process
        self.build_ok = build_ok

    def on_modified(self, event: Any) -> None:
        is_not_vendor = "vendor/" not in event.src_path
        if (
            is_not_vendor
            and not event.is_directory
            and any(event.src_path.endswith(ext) for ext in [".datasource", ".pipe", ".ndjson"])
        ):
            filename = event.src_path.split("/")[-1]
            click.echo(FeedbackManager.highlight(message=f"\n\n⟲ Changes detected in {filename}\n"))
            try:
                to_process = [event.src_path] if self.build_ok else self.filenames
                self.process(to_process)
                self.build_ok = True
            except Exception as e:
                click.echo(FeedbackManager.error_exception(error=e))


def watch_files(
    filenames: List[str],
    process: Callable,
    shell: Shell,
    folder: str,
    build_ok: bool,
) -> None:
    # Handle both sync and async process functions
    async def process_wrapper(files: List[str]) -> None:
        click.echo("⚡ Rebuilding...")
        time_start = time.time()
        if asyncio.iscoroutinefunction(process):
            await process(files, watch=True)
        else:
            process(files, watch=True)
        time_end = time.time()
        elapsed_time = time_end - time_start
        click.echo(
            FeedbackManager.success(message="\n✓ ")
            + FeedbackManager.gray(message=f"Rebuild completed in {elapsed_time:.1f}s")
        )
        shell.reprint_prompt()

    event_handler = FileChangeHandler(filenames, lambda f: asyncio.run(process_wrapper(f)), build_ok)
    observer = Observer()

    observer.schedule(event_handler, path=folder, recursive=True)

    observer.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()

    observer.join()
