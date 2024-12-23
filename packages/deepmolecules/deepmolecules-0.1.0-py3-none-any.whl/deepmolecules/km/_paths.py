from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from pathlib import Path

__all__ = [
    "_all_substrates_file",
    "_check_if_data_exists",
    "_gnn_input_dir",
    "_gnn_weights_dir",
    "_mol_feature_vectors_dir",
    "_mol_file_dir",
    "_xgboost_model_file",
]


def _mol_feature_vectors_dir(tmp_dir: Path) -> Path:
    path = tmp_dir / "mol_feature_vectors"
    path.mkdir(exist_ok=True, parents=True)
    return path


def _gnn_input_dir(tmp_dir: Path) -> Path:
    path = tmp_dir / "gnn_input_data"
    path.mkdir(exist_ok=True, parents=True)
    return path


def _gnn_weights_dir(data_dir: Path, *, create: bool = True) -> Path:
    path = data_dir / "gnn-weights"
    if create:
        path.mkdir(exist_ok=True, parents=True)
    return path


def _mol_file_dir(data_dir: Path, *, create: bool = True) -> Path:
    path = data_dir / "mol-files"
    if create:
        path.mkdir(exist_ok=True, parents=True)
    return path


def _all_substrates_file(data_dir: Path, *, create: bool = True) -> Path:
    path = data_dir / "all_substrates.pkl"
    if create:
        path.parent.mkdir(exist_ok=True, parents=True)
    return path


def _xgboost_model_file(data_dir: Path, *, create: bool = True) -> Path:
    path = data_dir / "esm1b_new_km.dat"
    if create:
        path.parent.mkdir(exist_ok=True, parents=True)
    return path


def _check_if_data_exists(data_dir: Path) -> None:
    if not _gnn_weights_dir(data_dir, create=False).exists():
        msg = "GNN weights missing. Download using `deepmolecules.download_data()`"
        raise ValueError(msg)
    if not _mol_file_dir(data_dir, create=False).exists():
        msg = "Mol files missing. Download using `deepmolecules.download_data()`"
        raise ValueError(msg)
    if not _all_substrates_file(data_dir, create=False).exists():
        msg = "All substrates file missing. Download using `deepmolecules.download_data()`"
        raise ValueError(msg)
    if not _xgboost_model_file(data_dir, create=False).exists():
        msg = "xgboost model missing. Download using `deepmolecules.download_data()`"
        raise ValueError(msg)
