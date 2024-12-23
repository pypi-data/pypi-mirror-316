from pathlib import Path
from tempfile import TemporaryDirectory

import numpy as np
from deepmolecules._shared_paths import _default_data_dir
from deepmolecules.km import _atom_and_bond_feature_vectors, _metabolite_preprocessing

data_dir = _default_data_dir(None)


def test_atom_and_bond_feature_vectors() -> None:
    with TemporaryDirectory() as tmp_dir:
        df = _atom_and_bond_feature_vectors(
            ["C00001", "C00002"],
            tmp_dir=Path(tmp_dir),
            data_dir=data_dir,
        )

    np.testing.assert_array_equal(
        df.columns.to_numpy(),
        ["metabolite", "number_atoms", "MW", "LogP", "metabolite_similarity_score"],
    )

    np.testing.assert_array_equal(
        df["metabolite"].to_numpy(),
        np.array(["C00001", "C00002"], dtype=object),
    )

    np.testing.assert_array_equal(
        df["number_atoms"].to_numpy(),
        np.array([1.0, 31.0], dtype=float),
    )

    np.testing.assert_array_almost_equal(
        df["MW"].to_numpy(),
        np.array([18.01, 506.99], dtype=float),
        decimal=2,
    )

    np.testing.assert_array_almost_equal(
        df["LogP"].to_numpy(),
        np.array([-0.8247, -1.629], dtype=float),
        decimal=2,
    )

    np.testing.assert_array_almost_equal(
        df["metabolite_similarity_score"].to_numpy(),
        np.array([1.0, 1.0], dtype=float),
        decimal=2,
    )


def test_metabolite_preprocessing() -> None:
    with TemporaryDirectory() as tmp_dir:
        df = _metabolite_preprocessing(
            ["C00001", "C00002"],
            tmp_dir=Path(tmp_dir),
            data_dir=data_dir,
        )

    np.testing.assert_array_equal(
        df.columns.to_numpy(),
        [
            "metabolite",
            "number_atoms",
            "MW",
            "LogP",
            "metabolite_similarity_score",
            "successfull",
        ],
    )

    np.testing.assert_array_equal(
        df["metabolite"].to_numpy(),
        np.array(["C00001", "C00002"], dtype=object),
    )

    np.testing.assert_array_equal(
        df["number_atoms"].to_numpy(),
        np.array([1.0, 31.0], dtype=float),
    )

    np.testing.assert_array_almost_equal(
        df["MW"].to_numpy(),
        np.array([18.01, 506.99], dtype=float),
        decimal=2,
    )

    np.testing.assert_array_almost_equal(
        df["LogP"].to_numpy(),
        np.array([-0.8247, -1.629], dtype=float),
        decimal=2,
    )

    np.testing.assert_array_almost_equal(
        df["metabolite_similarity_score"].to_numpy(),
        np.array([1.0, 1.0], dtype=float),
        decimal=2,
    )
