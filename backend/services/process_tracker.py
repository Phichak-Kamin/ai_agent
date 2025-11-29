"""Async helpers for simulating machine runtime and tracking durations."""
from __future__ import annotations

import asyncio
import time
from collections import defaultdict
from dataclasses import dataclass, field
from typing import Dict


@dataclass
class ProcessTracker:
    """Tracks mock process windows per machine."""

    active_runs: Dict[str, float] = field(default_factory=dict)
    durations: Dict[str, float] = field(default_factory=lambda: defaultdict(float))

    def start(self, machine: str) -> None:
        self.active_runs[machine] = time.monotonic()

    def stop(self, machine: str) -> float:
        start_time = self.active_runs.pop(machine, None)
        if start_time is None:
            return 0.0
        elapsed = time.monotonic() - start_time
        self.durations[machine] += elapsed
        return elapsed

    def summarize(self) -> Dict[str, float]:
        return dict(self.durations)


async def simulate_processing(duration_seconds: float) -> None:
    """Simple awaitable used by machine tools to emulate work."""

    await asyncio.sleep(duration_seconds)
