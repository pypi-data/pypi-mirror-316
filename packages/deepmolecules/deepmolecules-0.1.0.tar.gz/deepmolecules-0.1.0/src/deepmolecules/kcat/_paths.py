from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from pathlib import Path

__all__ = [
    "_esm1b_epoch_file",
    "_esm1b_train_test_file",
    "_mol_file_dir",
    "_xgboost_model_file",
    "_xgboost_regression_file",
]


def _mol_file_dir(data_dir: Path, *, create: bool = True) -> Path:
    path = data_dir / "mol-files"
    if create:
        path.mkdir(exist_ok=True, parents=True)
    return path


def _xgboost_model_file(data_dir: Path, *, create: bool = True) -> Path:
    path = data_dir / "esm1b_t33_650M_UR50S.pt"
    if create:
        path.parent.mkdir(exist_ok=True, parents=True)
    return path


def _xgboost_regression_file(data_dir: Path, *, create: bool = True) -> Path:
    path = data_dir / "esm1b_t33_650M_UR50S-contact-regression.pt"
    if create:
        path.parent.mkdir(exist_ok=True, parents=True)
    return path


def _esm1b_epoch_file(data_dir: Path, *, create: bool = True) -> Path:
    path = data_dir / "model_ESM_binary_A100_epoch_1_new_split.pkl"
    if create:
        path.parent.mkdir(exist_ok=True, parents=True)
    return path


def _esm1b_train_test_file(data_dir: Path, *, create: bool = True) -> Path:
    path = data_dir / "xgboost_train_and_test.pkl"
    if create:
        path.parent.mkdir(exist_ok=True, parents=True)
    return path


def _check_if_data_exists(data_dir: Path) -> None:
    if not _mol_file_dir(data_dir, create=False).exists():
        msg = "GNN weights missing. Download using `deepmolecules.download_data()`"
        raise ValueError(msg)
    if not _xgboost_model_file(data_dir, create=False).exists():
        msg = "Mol files missing. Download using `deepmolecules.download_data()`"
        raise ValueError(msg)
    if not _xgboost_regression_file(data_dir, create=False).exists():
        msg = "All substrates file missing. Download using `deepmolecules.download_data()`"
        raise ValueError(msg)
    if not _esm1b_epoch_file(data_dir, create=False).exists():
        msg = "xgboost model missing. Download using `deepmolecules.download_data()`"
        raise ValueError(msg)
    if not _esm1b_train_test_file(data_dir, create=False).exists():
        msg = "xgboost model missing. Download using `deepmolecules.download_data()`"
        raise ValueError(msg)
