from __future__ import annotations

import shutil
from pathlib import Path

__all__ = [
    "_default_data_dir",
    "_default_tmp_dir",
]


def _default_data_dir(data_dir: Path | None) -> Path:
    if data_dir is None:
        data_dir = Path.home() / ".cache" / "deepmolecules" / "data"

    data_dir.mkdir(exist_ok=True, parents=True)
    return data_dir


def _default_tmp_dir(
    tmp_dir: Path | None,
    *,
    remove_old_cache: bool,
) -> Path:
    if tmp_dir is None:
        tmp_dir = Path.home() / ".cache" / "deepmolecules" / "run"

    if tmp_dir.exists() and remove_old_cache:
        shutil.rmtree(tmp_dir)

    tmp_dir.mkdir(exist_ok=True, parents=True)
    return tmp_dir
