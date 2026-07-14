"""Shared provenance and artifact helpers for the Paper 1 RQ notebooks."""

from __future__ import annotations

import hashlib
import json
import os
import platform
import subprocess
import sys
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import yaml


PAPER_ROOT = Path(__file__).resolve().parents[1]


def _git(*args: str) -> str:
    return subprocess.check_output(
        ["git", *args], cwd=PAPER_ROOT, text=True, stderr=subprocess.DEVNULL
    ).strip()


def load_config(relative_path: str) -> tuple[Path, dict[str, Any], str]:
    path = PAPER_ROOT / relative_path
    raw = path.read_bytes()
    return path, yaml.safe_load(raw), hashlib.sha256(raw).hexdigest()


@dataclass(frozen=True)
class RunContext:
    track: str
    experiment_id: str
    run_id: str
    config_paths: tuple[Path, ...]
    configs: tuple[dict[str, Any], ...]
    config_digests: tuple[str, ...]
    result_dir: Path
    data_dir: Path
    table_dir: Path
    figure_dir: Path


def begin_run(
    track: str, config_relative_paths: list[str], run_id: str | None = None
) -> RunContext:
    loaded = [load_config(path) for path in config_relative_paths]
    config_paths = tuple(item[0] for item in loaded)
    configs = tuple(item[1] for item in loaded)
    digests = tuple(item[2] for item in loaded)
    experiment_ids = {config["experiment_id"] for config in configs}
    if len(experiment_ids) != 1:
        raise ValueError(f"Configs span multiple experiment families: {experiment_ids}")
    experiment_id = experiment_ids.pop()
    for path, config in zip(config_paths, configs):
        declared = config.get("research_question")
        if declared != track:
            raise ValueError(f"{path} belongs to {declared}, not {track}")
    combined_digest = hashlib.sha256("".join(digests).encode()).hexdigest()
    if run_id is None:
        stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
        run_id = f"{stamp}-{combined_digest[:8]}"
    result_dir = PAPER_ROOT / "results" / experiment_id / run_id
    if result_dir.exists():
        raise FileExistsError(f"Raw run already exists and is immutable: {result_dir}")
    data_dir = result_dir / "data"
    table_dir = PAPER_ROOT / "tables" / "generated" / track / run_id
    figure_dir = PAPER_ROOT / "figures" / "generated" / track / run_id
    for path in (data_dir, table_dir, figure_dir):
        path.mkdir(parents=True, exist_ok=False if path == data_dir else True)
    context = RunContext(
        track=track,
        experiment_id=experiment_id,
        run_id=run_id,
        config_paths=config_paths,
        configs=configs,
        config_digests=digests,
        result_dir=result_dir,
        data_dir=data_dir,
        table_dir=table_dir,
        figure_dir=figure_dir,
    )
    write_metadata(context, status="started")
    return context


def write_metadata(context: RunContext, *, status: str, **updates: Any) -> Path:
    metadata_path = context.result_dir / "run.json"
    metadata = {
        "track": context.track,
        "experiment_id": context.experiment_id,
        "run_id": context.run_id,
        "code_revision": _git("rev-parse", "HEAD"),
        "dirty_worktree": bool(_git("status", "--porcelain")),
        "config_paths": [str(path.relative_to(PAPER_ROOT)) for path in context.config_paths],
        "config_digests": list(context.config_digests),
        "random_seeds": [config.get("seed") for config in context.configs],
        "environment": {"python": sys.version, "executable": sys.executable},
        "hardware": {"platform": platform.platform(), "cpu_count": os.cpu_count()},
        "status": status,
        **updates,
    }
    metadata_path.write_text(json.dumps(metadata, indent=2, sort_keys=True) + "\n")
    return metadata_path


def save_dataframe(frame: Any, path: Path) -> Path:
    """Save a pandas-like dataframe as CSV without mutating raw inputs."""
    path.parent.mkdir(parents=True, exist_ok=True)
    frame.to_csv(path, index=False)
    return path


def save_figure(figure: Any, path: Path) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    figure.savefig(path, bbox_inches="tight", dpi=300)
    return path
