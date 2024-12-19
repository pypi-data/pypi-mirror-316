from rich.console import Console
from rich.traceback import install as tr_install

from loguru_rich_sink.__main__ import logger, on_exit
from loguru_rich_sink.sink import increment, read, rich_sink, setup, write

console = Console()
tr_install(console=console)

__all__ = ["rich_sink", "setup", "read", "write", "increment", "on_exit", "logger"]

setup()
