import asyncio
import concurrent.futures
import os
import random
import subprocess
import sys
from typing import List

import click
import humanfriendly
from prompt_toolkit import PromptSession
from prompt_toolkit.completion import Completer, Completion
from prompt_toolkit.history import FileHistory
from prompt_toolkit.key_binding import KeyBindings
from prompt_toolkit.shortcuts import CompleteStyle
from prompt_toolkit.styles import Style

from tinybird.client import TinyB
from tinybird.feedback_manager import FeedbackManager, bcolors
from tinybird.tb.modules.exceptions import CLIException
from tinybird.tb.modules.table import format_table


class DynamicCompleter(Completer):
    def __init__(self, datasources: List[str], pipes: List[str]):
        self.datasources = datasources
        self.pipes = pipes
        self.static_commands = ["create", "mock", "test", "select"]
        self.mock_flags = ["--prompt", "--rows"]
        self.common_rows = ["10", "50", "100", "500", "1000"]
        self.sql_keywords = ["select", "from", "where", "group by", "order by", "limit"]

    def get_completions(self, document, complete_event):
        text = document.text_before_cursor.strip()
        words = text.split()

        # Normalize command by removing 'tb' prefix if present
        if words and words[0] == "tb":
            words = words[1:]

        if not words:
            # Show all available commands when no input
            yield from self._yield_static_commands("")
            return

        command = words[0].lower()

        if command == "mock":
            yield from self._handle_mock_completions(words)
        elif command == "select" or self._is_sql_query(text.lower()):
            yield from self._handle_sql_completions(text)
        else:
            # Handle general command completions
            yield from self._yield_static_commands(words[-1])

    def _is_sql_query(self, text: str) -> bool:
        """Check if the input looks like a SQL query."""
        sql_starters = ["select", "with"]
        return any(text.startswith(starter) for starter in sql_starters)

    def _handle_sql_completions(self, text: str):
        """Handle completions for SQL queries."""
        text_lower = text.lower()

        # Find the last complete word
        words = text_lower.split()
        if not words:
            return

        # If we just typed 'from' or there's a space after 'from', suggest datasources
        if words[-1] == "from" or (
            "from" in words and len(words) > words.index("from") + 1 and text_lower.endswith(" ")
        ):
            for x in self.datasources:
                yield Completion(x, start_position=0, display=x, style="class:completion.datasource")
            for x in self.pipes:
                yield Completion(x, start_position=0, display=x, style="class:completion.pipe")
            return

        # If we're starting a query, suggest SQL keywords
        if len(words) <= 2:
            for keyword in self.sql_keywords:
                if keyword.lower().startswith(words[-1]):
                    yield Completion(
                        keyword, start_position=-len(words[-1]), display=keyword, style="class:completion.keyword"
                    )

    def _handle_mock_completions(self, words: List[str]):
        if len(words) == 1:
            # After 'mock', show datasources
            for ds in self.datasources:
                yield Completion(ds, start_position=0, display=ds, style="class:completion.cmd")
            return

        if len(words) == 2 or len(words) == 4:
            # After datasource or after a flag value, show available flags
            available_flags = [f for f in self.mock_flags if f not in words]
            for flag in available_flags:
                yield Completion(flag, start_position=0, display=flag)
            return

        last_word = words[-1]
        if last_word == "--prompt":
            yield Completion('""', start_position=0, display='"Enter your prompt..."')
        elif last_word == "--rows":
            for rows in self.common_rows:
                yield Completion(rows, start_position=0, display=rows)

    def _yield_static_commands(self, current_word: str):
        for cmd in self.static_commands:
            if cmd.startswith(current_word):
                yield Completion(
                    cmd,
                    start_position=-len(current_word) if current_word else 0,
                    display=cmd,
                    style="class:completion.cmd",
                )


style = Style.from_dict(
    {
        "prompt": "fg:#34D399 bold",
        "completion.cmd": "fg:#34D399 bg:#111111 bold",
        "completion.datasource": "fg:#AB49D0 bg:#111111",
        "completion.pipe": "fg:#FEA827 bg:#111111",
        "completion.keyword": "fg:#34D399 bg:#111111",
    }
)

key_bindings = KeyBindings()


@key_bindings.add("c-d")
def _(event):
    """
    Start auto completion. If the menu is showing already, select the next
    completion.
    """
    b = event.app.current_buffer
    if b.complete_state:
        b.complete_next()
    else:
        b.start_completion(select_first=False)


class BuildShell:
    def __init__(self, folder: str, client: TinyB, datasources: List[str], pipes: List[str]):
        self.history = self.get_history()
        self.folder = folder
        self.client = client
        self.datasources = datasources
        self.pipes = pipes
        self.prompt_message = "\ntb > "
        self.commands = ["create", "mock", "test", "tb", "select"]

        self.session = PromptSession(
            completer=DynamicCompleter(self.datasources, self.pipes),
            complete_style=CompleteStyle.COLUMN,
            complete_while_typing=True,
            history=self.history,
        )

    def get_history(self):
        try:
            history_file = os.path.expanduser("~/.tb_history")
            return FileHistory(history_file)
        except Exception:
            return None

    def run_shell(self):
        while True:
            try:
                user_input = self.session.prompt(
                    [("class:prompt", self.prompt_message)], style=style, key_bindings=key_bindings
                )
                self.handle_input(user_input)
            except (EOFError, KeyboardInterrupt):
                sys.exit(0)
            except CLIException as e:
                click.echo(str(e))
            except Exception as e:
                # Catch-all for unexpected exceptions
                click.echo(FeedbackManager.error_exception(error=str(e)))

    def handle_input(self, argline):
        line = argline.strip()
        if not line:
            return

        # Implement the command logic here
        # Replace do_* methods with equivalent logic:
        command_parts = line.split(maxsplit=1)
        cmd = command_parts[0].lower()
        arg = command_parts[1] if len(command_parts) > 1 else ""

        if cmd in ["exit", "quit"]:
            sys.exit(0)
        elif cmd == "build":
            self.handle_build(arg)
        elif cmd == "auth":
            self.handle_auth(arg)
        elif cmd == "workspace":
            self.handle_workspace(arg)
        elif cmd == "mock":
            self.handle_mock(arg)
        elif cmd == "tb":
            self.handle_tb(arg)
        else:
            # Check if it looks like a SQL query or run as a tb command
            self.default(line)

    def handle_build(self, arg):
        click.echo(FeedbackManager.error(message=f"'tb {arg}' command is not available in watch mode"))

    def handle_auth(self, arg):
        click.echo(FeedbackManager.error(message=f"'tb {arg}' command is not available in watch mode"))

    def handle_workspace(self, arg):
        click.echo(FeedbackManager.error(message=f"'tb {arg}' command is not available in watch mode"))

    def handle_mock(self, arg):
        subprocess.run(f"tb mock {arg} --folder {self.folder}", shell=True, text=True)

    def handle_tb(self, arg):
        click.echo("")
        arg = arg.strip().lower()
        if arg.startswith("build"):
            self.handle_build(arg)
        elif arg.startswith("auth"):
            self.handle_auth(arg)
        elif arg.startswith("workspace"):
            self.handle_workspace(arg)
        elif arg.startswith("mock"):
            self.handle_mock(arg)
        else:
            subprocess.run(f"tb --local {arg}", shell=True, text=True)

    def default(self, argline):
        click.echo("")
        arg = argline.strip().lower()
        if not arg:
            return
        if arg.startswith("with") or arg.startswith("select"):
            try:
                self.run_sql(argline)
            except Exception as e:
                click.echo(FeedbackManager.error(message=str(e)))
        else:
            subprocess.run(f"tb --local {arg}", shell=True, text=True)

    def run_sql(self, query, rows_limit=20):
        try:
            q = query.strip()
            if q.lower().startswith("insert"):
                click.echo(FeedbackManager.info_append_data())
                raise CLIException(FeedbackManager.error_invalid_query())
            if q.lower().startswith("delete"):
                raise CLIException(FeedbackManager.error_invalid_query())

            def run_query_in_thread():
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)
                try:
                    return loop.run_until_complete(
                        self.client.query(f"SELECT * FROM ({query}) LIMIT {rows_limit} FORMAT JSON")
                    )
                finally:
                    loop.close()

            with concurrent.futures.ThreadPoolExecutor() as executor:
                res = executor.submit(run_query_in_thread).result()

        except Exception as e:
            raise CLIException(FeedbackManager.error_exception(error=str(e)))

        if isinstance(res, dict) and "error" in res:
            raise CLIException(FeedbackManager.error_exception(error=res["error"]))

        if isinstance(res, dict) and "data" in res and res["data"]:
            print_table_formatted(res, "QUERY")
        else:
            click.echo(FeedbackManager.info_no_rows())

    def reprint_prompt(self):
        click.echo(f"{bcolors.OKGREEN}{self.prompt_message}{bcolors.ENDC}", nl=False)


def print_table_formatted(res: dict, name: str):
    rebuild_colors = [bcolors.FAIL, bcolors.OKBLUE, bcolors.WARNING, bcolors.OKGREEN, bcolors.HEADER]
    rebuild_index = random.randint(0, len(rebuild_colors) - 1)
    rebuild_color = rebuild_colors[rebuild_index % len(rebuild_colors)]
    data = []
    limit = 5
    for d in res["data"][:5]:
        data.append(d.values())
    meta = res["meta"]
    row_count = res.get("rows", 0)
    stats = res.get("statistics", {})
    elapsed = stats.get("elapsed", 0)
    cols = len(meta)
    try:

        def print_message(message: str, color=bcolors.CGREY):
            return f"{color}{message}{bcolors.ENDC}"

        table = format_table(data, meta)
        colored_char = print_message("│", rebuild_color)
        table_with_marker = "\n".join(f"{colored_char} {line}" for line in table.split("\n"))
        click.echo(f"\n{colored_char} {print_message('⚡', rebuild_color)} Running {name}")
        click.echo(colored_char)
        click.echo(table_with_marker)
        click.echo(colored_char)
        rows_read = humanfriendly.format_number(stats.get("rows_read", 0))
        bytes_read = humanfriendly.format_size(stats.get("bytes_read", 0))
        elapsed = humanfriendly.format_timespan(elapsed) if elapsed >= 1 else f"{elapsed * 1000:.2f}ms"
        stats_message = f"» {bytes_read} ({rows_read} rows x {cols} cols) in {elapsed}"
        rows_message = f"» Showing {limit} first rows" if row_count > limit else "» Showing all rows"
        click.echo(f"{colored_char} {print_message(stats_message, bcolors.OKGREEN)}")
        click.echo(f"{colored_char} {print_message(rows_message, bcolors.CGREY)}")
    except ValueError as exc:
        if str(exc) == "max() arg is an empty sequence":
            click.echo("------------")
            click.echo("Empty")
            click.echo("------------")
        else:
            raise exc
