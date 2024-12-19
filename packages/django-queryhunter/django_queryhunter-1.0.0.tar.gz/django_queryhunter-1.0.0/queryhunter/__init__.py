from pathlib import Path

from .context_manager import queryhunter
from .reporting import (
    ReportingOptions,
    LoggingOptions,
    PrintingOptions,
)


def default_base_dir(file) -> str:
    return str(Path(file).resolve().parent.parent)


