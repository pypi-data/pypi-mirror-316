from __future__ import annotations

from logging import getLogger
from pathlib import Path

from tqdm import tqdm

from ._shared_paths import _default_data_dir

__all__ = ["download_data"]

logger = getLogger("deepmolecules")


def _unzip(path: Path) -> None:
    import zipfile

    with zipfile.ZipFile(path, "r") as fp:
        fp.extractall(path.parent)


def _download_file(url: str, file: Path, chunk_size: int = 1024) -> Path:
    import requests

    if file.exists():
        logger.info("File exists %s", file)
        return file

    logger.info("Downloading %s", file)

    resp = requests.get(url, stream=True, timeout=60)
    total = int(resp.headers.get("content-length", 0))

    with (
        file.open("wb") as f,
        tqdm(
            desc=url,
            total=total,
            miniters=1,
            unit="B",
            unit_scale=True,
            unit_divisor=1024,
        ) as pb,
    ):
        for data in resp.iter_content(chunk_size=chunk_size):
            size = f.write(data)
            pb.update(size)

    if file.suffix == ".zip":
        _unzip(file)

    return file


def download_data(
    data_dir: Path | None = None,
    *,
    remove_download: bool = True,
) -> None:
    from torch import hub

    import deepmolecules.kcat._paths as kcat_paths
    import deepmolecules.km._paths as km_paths

    data_dir = _default_data_dir(data_dir)

    try:
        km_paths._check_if_data_exists(data_dir)  # noqa: SLF001
        kcat_paths._check_if_data_exists(data_dir)  # noqa: SLF001
        logger.info("Data already exists at %s", data_dir)

    except ValueError:
        logger.info("Downloading data to %s", data_dir)

        file = _download_file(
            url="https://zenodo.org/records/11236283/files/data.zip?download=1",
            file=data_dir / "download.zip",
        )

        if remove_download:
            file.unlink()

    # Download ESM-1b model
    if not (
        Path(hub.DEFAULT_CACHE_DIR).expanduser()
        / "torch"
        / "hub"
        / "facebookresearch_esm_v0.4.0"
    ).exists():
        logger.info("Downloading ESM1B model")
        hub.load("facebookresearch/esm:v0.4.0", "esm1b_t33_650M_UR50S")
