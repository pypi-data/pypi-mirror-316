from __future__ import annotations

import asyncio
import logging
from typing import TYPE_CHECKING
from weakref import WeakSet


if TYPE_CHECKING:
    from llmling_agent.commands.base import OutputWriter


class SessionLogHandler(logging.Handler):
    """Captures logs for display in chat session."""

    def __init__(self, output_writer: OutputWriter) -> None:
        super().__init__()
        self.output_writer = output_writer
        self.setFormatter(logging.Formatter("📝 [%(levelname)s] %(message)s"))
        self._tasks: WeakSet[asyncio.Task] = WeakSet()

    def emit(self, record: logging.LogRecord) -> None:
        try:
            msg = self.format(record)
            task = asyncio.create_task(self.output_writer.print(msg))
            self._tasks.add(task)
            # Optional: Add done callback to remove completed tasks
            task.add_done_callback(self._tasks.discard)
        except Exception:  # noqa: BLE001
            self.handleError(record)

    async def wait_for_tasks(self) -> None:
        """Wait for all pending log output tasks to complete."""
        if self._tasks:
            await asyncio.gather(*self._tasks, return_exceptions=True)
