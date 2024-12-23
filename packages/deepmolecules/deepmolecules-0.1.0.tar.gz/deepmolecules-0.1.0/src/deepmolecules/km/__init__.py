from __future__ import annotations

import pickle
import warnings
from logging import getLogger
from typing import TYPE_CHECKING, Any, cast

import esm
import numpy as np
import pandas as pd
import tensorflow as tf
import torch
import xgboost as xgb
from keras import backend, layers
from keras.activations import relu
from keras.layers import (
    BatchNormalization,
    Concatenate,
    Dropout,
    Input,
    add,
)
from keras.losses import MSE
from keras.models import Model
from keras.optimizers.legacy import Adadelta
from rdkit import DataStructs
from rdkit.Chem import Crippen, Descriptors
from rdkit.Chem.rdmolops import (
    RDKFingerprint,
)

from deepmolecules._chem import _get_mol
from deepmolecules._shared_paths import _default_data_dir, _default_tmp_dir

from ._constants import (
    AROMATIC,
    ATOMIC_NUMBER,
    BOND_TYPE,
    CHARGE,
    CHIRALITY,
    CONJUGATED,
    F1,
    H_BONDS,
    HYBRID,
    IN_RING,
    NUM_BONDS,
    STEREO,
    F,
)
from ._paths import (
    _all_substrates_file,
    _check_if_data_exists,
    _gnn_input_dir,
    _gnn_weights_dir,
    _mol_feature_vectors_dir,
    _mol_file_dir,
    _xgboost_model_file,
)

__all__ = ["Linear", "LinearWithBias", "crop_sequence", "predict", "preprocess_enzymes"]

if TYPE_CHECKING:
    from collections.abc import Callable, Hashable, Iterable
    from pathlib import Path

    from rdkit.Chem.rdchem import Mol


logger = getLogger("deepmolecules")

warnings.filterwarnings("ignore")


class Linear(layers.Layer):
    def __init__(self, dim: Iterable[int] = (1, 1, 42, 64)) -> None:
        super().__init__()
        w_init = tf.random_normal_initializer()
        self.w = tf.Variable(
            initial_value=w_init(shape=(dim), dtype=tf.float32),
            trainable=True,
        )

    def call(self, inputs: Any) -> Any:
        return tf.matmul(inputs, self.w)


class LinearWithBias(layers.Layer):
    def __init__(self, dim: Iterable[int]) -> None:
        super().__init__()
        w_init = tf.random_normal_initializer()
        b_init = tf.constant_initializer(0.1)  # type: ignore (should be int is float)
        self.w = tf.Variable(
            initial_value=w_init(shape=(dim), dtype=tf.float32),
            trainable=True,
        )

        self.b = tf.Variable(
            initial_value=b_init(shape=[self.w.shape[-1]], dtype=tf.float32),
            trainable=True,
        )

    def call(self, inputs: Any) -> Any:
        return tf.math.add(tf.matmul(inputs, self.w), self.b)


def _atom_feature_vector_for_mol(mol: Mol) -> list[Any]:
    atom_list = []
    for i in range(mol.GetNumAtoms()):
        atom = mol.GetAtomWithIdx(i)
        atom_list.append(
            [
                atom.GetAtomicNum(),
                atom.GetDegree(),
                atom.GetFormalCharge(),
                str(atom.GetHybridization()),
                atom.GetIsAromatic(),
                atom.GetMass(),
                atom.GetTotalNumHs(),
                str(atom.GetChiralTag()),
            ],
        )
    return atom_list


def _bond_feature_vector_for_mol(mol: Mol) -> list[Any]:
    bond_list = []
    for i in range(mol.GetNumBonds()):
        bond = mol.GetBondWithIdx(i)
        bond_list.append(
            [
                bond.GetBeginAtomIdx(),
                bond.GetEndAtomIdx(),
                str(bond.GetBondType()),
                bond.GetIsAromatic(),
                bond.IsInRing(),
                str(bond.GetStereo()),
            ],
        )
    return bond_list


def _metabolite_similarity(*, all_fingerprints: pd.DataFrame, mol: Mol) -> float:
    fp = RDKFingerprint(mol)
    return max(DataStructs.FingerprintSimilarity(fp, i) for i in all_fingerprints)


def _concatenate_x_and_e(
    x: np.ndarray,
    e: np.ndarray,
    n: int,
    f: int = 32 + 10,
) -> np.ndarray:
    xe = np.zeros((n, n, f))
    for v in range(n):
        x_v = x[v, :]
        for w in range(n):
            xe[v, w, :] = np.concatenate((x_v, e[v, w, :]))
    return xe


def _load_bond_features(
    met_id: Hashable,
    n: int,
    tmp_dir: Path,
) -> tuple[np.ndarray, np.ndarray] | tuple[None, None]:
    """Create adjacency matrix A and bond feature matrix/tensor E"""
    path = _mol_feature_vectors_dir(tmp_dir=tmp_dir) / f"{met_id}_bonds.txt"
    if not path.exists():
        return None, None

    with path.open("rb") as fp:
        bond_features = pickle.load(fp)

    a = np.zeros((n, n))
    e = np.zeros((n, n, 10))
    for i in range(len(bond_features)):
        line = bond_features[i]
        start, end = line[0], line[1]
        a[start, end] = 1
        a[end, start] = 1
        e_vw = np.concatenate(
            (
                BOND_TYPE[line[2]],
                CONJUGATED[line[3]],
                IN_RING[line[4]],
                STEREO[line[5]],
            ),
        )
        e[start, end, :] = e_vw
        e[end, start, :] = e_vw
    return a, e


def _load_atom_features(
    mol_name: Hashable,
    n: int,
    tmp_dir: Path,
) -> np.ndarray | None:
    path = _mol_feature_vectors_dir(tmp_dir=tmp_dir) / f"{mol_name}_atoms.txt"
    if not path.exists():
        return None

    with path.open("rb") as fp:
        atom_features = pickle.load(fp)

    x = np.zeros((n, 32))
    if len(atom_features) >= n:
        return None
    for i in range(len(atom_features)):
        line = atom_features[i]
        x_v = np.concatenate(
            (
                ATOMIC_NUMBER[line[0]],
                NUM_BONDS[line[1]],
                CHARGE[line[2]],
                HYBRID[line[3]],
                AROMATIC[line[4]],
                np.array([line[5] / 100.0]),
                H_BONDS[line[6]],
                CHIRALITY[line[7]],
            ),
        )
        x[i, :] = x_v
    return x


def _input_data_for_gnn_for_substrates(
    substrate_id: Hashable,
    n_max: int,
    tmp_dir: Path,
) -> tuple[np.ndarray, np.ndarray, np.ndarray] | tuple[None, None, None]:
    x = _load_atom_features(mol_name=substrate_id, n=n_max, tmp_dir=tmp_dir)
    if x is None:
        return None, None, None

    a, e = _load_bond_features(met_id=substrate_id, n=n_max, tmp_dir=tmp_dir)
    if a is None or e is None:
        return None, None, None

    a = np.reshape(a, (n_max, n_max, 1))
    xe = _concatenate_x_and_e(x, e, n=n_max)
    return np.array(xe), np.array(x), np.array(a)


def _atom_and_bond_feature_vectors(
    metabolites: list[str],
    tmp_dir: Path,
    data_dir: Path,
) -> pd.DataFrame:
    # Creating a temporary directory to save data for metabolites
    feature_vector_dir = _mol_feature_vectors_dir(tmp_dir=tmp_dir)
    mol_file_dir = _mol_file_dir(data_dir=data_dir)

    all_fingerprints = pd.read_pickle(_all_substrates_file(data_dir=data_dir))[
        "Sim_FP"
    ].to_numpy()

    mets = {}
    for i, met in enumerate(metabolites):
        mol = _get_mol(met, mol_file_dir)

        if mol is None:
            logger.info("Invalid metabolite %s", met)
            continue

        with (feature_vector_dir / f"{i}_atoms.txt").open("wb") as fp:
            pickle.dump(_atom_feature_vector_for_mol(mol), fp)

        with (feature_vector_dir / f"{i}_bonds.txt").open("wb") as fp:
            pickle.dump(_bond_feature_vector_for_mol(mol), fp)

        mets[i] = {
            "metabolite": met,
            "number_atoms": mol.GetNumAtoms(),
            "MW": Descriptors.ExactMolWt(mol),  # type: ignore
            "LogP": Crippen.MolLogP(mol),  # type: ignore
            "metabolite_similarity_score": _metabolite_similarity(
                all_fingerprints=all_fingerprints,
                mol=mol,
            ),
        }

    return pd.DataFrame(mets).T


def _save_input_matrices(
    mets: pd.DataFrame,
    n_max: int,
    tmp_dir: Path,
) -> None:
    gnn_input_dir = _gnn_input_dir(tmp_dir=tmp_dir)

    for i, met in mets.iterrows():
        extras = met[["MW", "LogP"]].to_numpy()
        xe, x, a = _input_data_for_gnn_for_substrates(
            substrate_id=i,
            n_max=n_max,
            tmp_dir=tmp_dir,
        )
        if a is not None and x is not None and xe is not None:
            np.save(gnn_input_dir / f"{i}_X.npy", x)
            np.save(gnn_input_dir / f"{i}_XE.npy", xe)
            np.save(gnn_input_dir / f"{i}_A.npy", a)
            np.save(gnn_input_dir / f"{i}_extras.npy", extras)
        else:
            raise ValueError


def _metabolite_preprocessing(
    metabolites: list[str],
    tmp_dir: Path,
    data_dir: Path,
) -> pd.DataFrame:
    mets = _atom_and_bond_feature_vectors(
        metabolites, tmp_dir=tmp_dir, data_dir=data_dir
    )
    _save_input_matrices(
        mets=mets,
        n_max=mets["number_atoms"].max() + 1,
        tmp_dir=tmp_dir,
    )
    # FIXME: remove the entire successfull handling
    mets["successfull"] = True
    return mets


def crop_sequence(seq: str, max_len: int) -> str:
    return seq[:max_len]


def preprocess_enzymes(enzymes: list[str]) -> pd.DataFrame:
    df_enzyme = pd.DataFrame(data={"amino acid sequence": list(set(enzymes))})
    df_enzyme.index = ["protein_" + str(ind) for ind in df_enzyme.index]
    df_enzyme["model_input"] = [
        crop_sequence(seq, 1022) for seq in df_enzyme["amino acid sequence"]
    ]
    return df_enzyme


def _esm1b_vectors(enzymes: list[str]) -> pd.DataFrame:
    df_enzyme = preprocess_enzymes(enzymes)

    model, alphabet = esm.pretrained.esm1b_t33_650M_UR50S()
    batch_converter = alphabet.get_batch_converter()

    enzyme_reps = {}
    for idx, s in df_enzyme.iterrows():
        _, _, batch_tokens = batch_converter([(s.index, s["model_input"])])
        with torch.no_grad():
            enzyme_reps[idx] = (
                model(batch_tokens, repr_layers=[33])["representations"][33][
                    0,
                    1 : len(s["model_input"]) + 1,
                ]
                .mean(axis=0)
                .numpy()
            )
    df_enzyme["enzyme rep"] = enzyme_reps
    return df_enzyme


def _dmpnn(  # noqa: PLR0913
    n: float,
    l2_reg_conv: float = 0.01,
    l2_reg_fc: float = 1.0,
    learning_rate: float = 0.05,
    d: int = 50,
    f1: int = F1,
    f: int = F,
    drop_rate: float = 0.0,
    ada_rho: float = 0.95,
) -> Model:
    """Directed message passing neural network"""
    # Model definition
    XE_in = Input(shape=(n, n, f), name="XE", dtype=float)
    X_in = Input(shape=(n, f1), dtype=float)
    Extras_in = Input((2), name="Extras", dtype=float)

    X = tf.reshape(X_in, (-1, n, 1, f1))
    A_in = Input(
        (n, n, 1),
        name="A",
        dtype=float,
    )  # 64 copies of A stacked behind each other
    Wi = Linear((1, 1, f, d))
    Wm1 = Linear((1, 1, d, d))
    Wm2 = Linear((1, 1, d, d))
    Wa = Linear((1, d + f1, d))

    W_fc1 = LinearWithBias((d + 2, 32))
    W_fc2 = LinearWithBias((32, 16))
    W_fc3 = LinearWithBias((16, 1))

    OnesN_N = tf.ones((n, n))
    Ones1_N = tf.ones((1, n))

    H0 = relu(Wi(XE_in))  # W*XE

    # only get neighbors in each row: (elementwise multiplication)
    M1 = tf.multiply(H0, A_in)
    M1 = tf.transpose(M1, perm=[0, 2, 1, 3])
    M1 = tf.matmul(OnesN_N, M1)
    M1 = add(inputs=[M1, -tf.transpose(H0, perm=[0, 2, 1, 3])])
    M1 = tf.multiply(M1, A_in)
    H1 = add(inputs=[H0, Wm1(M1)])
    H1 = relu(BatchNormalization(momentum=0.90, trainable=True)(H1))

    M2 = tf.multiply(H1, A_in)
    M2 = tf.transpose(M2, perm=[0, 2, 1, 3])
    M2 = tf.matmul(OnesN_N, M2)
    M2 = add(inputs=[M2, -tf.transpose(H1, perm=[0, 2, 1, 3])])
    M2 = tf.multiply(M2, A_in)
    H2 = add(inputs=[H0, Wm2(M2)])
    H2 = relu(BatchNormalization(momentum=0.90, trainable=True)(H2))

    M_v = tf.multiply(H2, A_in)
    M_v = tf.matmul(Ones1_N, M_v)
    XM = Concatenate()(inputs=[X, M_v])
    H = relu(Wa(XM))
    h = tf.matmul(Ones1_N, tf.transpose(H, perm=[0, 2, 1, 3]))
    h = tf.reshape(h, (-1, d))
    h_extras = Concatenate()(inputs=[h, Extras_in])
    h_extras = BatchNormalization(momentum=0.90, trainable=True)(h_extras)

    fc1 = relu(W_fc1(h_extras))
    fc1 = BatchNormalization(momentum=0.90, trainable=True)(fc1)
    fc1 = Dropout(drop_rate)(fc1)

    fc2 = relu(W_fc2(fc1))
    fc2 = BatchNormalization(momentum=0.90, trainable=True)(fc2)

    output = W_fc3(fc2)

    def total_loss(y_true: Any, y_pred: Any) -> Any:
        reg_conv_loss = (
            tf.nn.l2_loss(Wi.w)
            + tf.nn.l2_loss(Wm1.w)
            + tf.nn.l2_loss(Wm2.w)
            + tf.nn.l2_loss(Wa.w)
        )
        reg_fc_loss = (
            tf.nn.l2_loss(W_fc1.w) + tf.nn.l2_loss(W_fc2.w) + tf.nn.l2_loss(W_fc3.w)
        )
        mse_loss = MSE(y_true, y_pred)
        return tf.reduce_mean(
            mse_loss + l2_reg_conv * reg_conv_loss + l2_reg_fc * reg_fc_loss,
        )

    model = Model(inputs=[XE_in, X_in, A_in, Extras_in], outputs=output)
    model.compile(
        optimizer=Adadelta(learning_rate=learning_rate, rho=ada_rho),
        loss=total_loss,
        metrics=["mse", "mae"],
    )
    return model


def _load_gnn(
    n: int,
    data_dir: Path,
) -> Callable:
    model = _dmpnn(n=n)
    model.load_weights(
        _gnn_weights_dir(data_dir=data_dir) / "saved_model_GNN_best_hyperparameters",
    )
    return backend.function(
        [
            model.layers[0].input,
            model.layers[26].input,
            model.layers[3].input,
            model.layers[36].input,
        ],
        [model.layers[-10].output],
    )


def _load_representation_input(
    cids: Iterable[str],
    tmp_dir: Path,
) -> tuple[list[np.ndarray], list[np.ndarray], list[np.ndarray], list[np.ndarray]]:
    gnn_path = _gnn_input_dir(tmp_dir=tmp_dir)
    return (
        [np.load(gnn_path / f"{cid}_XE.npy", allow_pickle=True) for cid in cids],
        [np.load(gnn_path / f"{cid}_X.npy", allow_pickle=True) for cid in cids],
        [np.load(gnn_path / f"{cid}_A.npy", allow_pickle=True) for cid in cids],
        [np.load(gnn_path / f"{cid}_extras.npy", allow_pickle=True) for cid in cids],
    )


def _metabolite_representations(
    df: pd.DataFrame,
    get_fingerprint_fct: Callable,
    tmp_dir: Path,
) -> pd.DataFrame:
    df["GNN rep"] = ""
    i = 0
    n = len(df)

    cid_all = df.index

    while i * 64 <= n:
        if (i + 1) * 64 <= n:
            XE, X, A, extras = _load_representation_input(
                cid_all[i * 64 : (i + 1) * 64],
                tmp_dir=tmp_dir,
            )
            representations = get_fingerprint_fct(
                [
                    np.array(XE, dtype=np.float32),
                    np.array(X, dtype=np.float32),
                    np.array(A, dtype=np.float32),
                    np.array(extras, dtype=np.float32),
                ],
            )[0]
            df["GNN rep"][i * 64 : (i + 1) * 64] = list(representations[:, :52])
        else:
            XE, X, A, extras = _load_representation_input(
                cid_all[i * 64 :],
                tmp_dir=tmp_dir,
            )
            representations = get_fingerprint_fct(
                [
                    np.array(XE, dtype=np.float32),
                    np.array(X, dtype=np.float32),
                    np.array(A, dtype=np.float32),
                    np.array(extras, dtype=np.float32),
                ],
            )[0]
            df["GNN rep"][i * 64 :] = list(representations[:, :52])
        i += 1
    return df


def _calculate_gnn_representations(
    df_met: pd.DataFrame,
    tmp_dir: Path,
    data_dir: Path,
) -> pd.DataFrame:
    N_max = np.max(df_met["number_atoms"].loc[df_met["successfull"]]) + 1
    GNN_representation_fct = _load_gnn(
        N_max,
        data_dir=data_dir,
    )

    df_valid_met = df_met.loc[df_met["successfull"]].reset_index(drop=True)
    df_invalid_met = df_met.loc[~df_met["successfull"]]

    df_valid_met = _metabolite_representations(
        df=df_valid_met,
        get_fingerprint_fct=GNN_representation_fct,
        tmp_dir=tmp_dir,
    )
    df_invalid_met["GNN rep"] = ""
    return pd.concat([df_valid_met, df_invalid_met], ignore_index=True)


def _predict_km(x: pd.DataFrame, data_dir: Path) -> np.ndarray:
    path = _xgboost_model_file(data_dir=data_dir)

    with path.open("rb") as fp:
        bst = cast(xgb.XGBClassifier, pickle.load(fp))

    return 10 ** bst.predict(xgb.DMatrix(x))


def _xgb_input_matrix(df: pd.DataFrame) -> pd.DataFrame:
    # FIXME: this is ugly and due to pandas setting object dtype on
    # the arrays. They probably should never have been in a dataframe
    # in the first place
    return cast(
        pd.DataFrame,
        np.concatenate(
            (np.array(list(df["GNN rep"])), np.array(list(df["enzyme rep"]))),
            axis=1,
        ),
    )


def _merge_dfs(
    metabolites: pd.DataFrame,
    enzymes: pd.DataFrame,
    kms: pd.DataFrame,
) -> pd.DataFrame:
    complete = []
    gnn_reps = []
    esm1b_reps = []

    for ind in kms.index:
        gnn_rep = next(
            iter(
                metabolites["GNN rep"].loc[
                    metabolites["metabolite"] == kms.loc[ind, "substrate"]
                ],
            ),
        )
        esm1b_rep = next(
            iter(
                enzymes["enzyme rep"].loc[
                    enzymes["amino acid sequence"] == kms.loc[ind, "enzyme"]
                ],
            ),
        )

        if len(gnn_rep) == 0 or len(esm1b_rep) == 0:
            complete.append(False)
            gnn_reps.append(np.array([], dtype=np.float32))
            esm1b_reps.append(np.array([], dtype=np.float32))

        else:
            complete.append(True)
            gnn_reps.append(gnn_rep)
            esm1b_reps.append(esm1b_rep)

    kms["GNN rep"] = gnn_reps
    kms["enzyme rep"] = esm1b_reps
    kms["complete"] = complete
    return kms


def predict(
    substrates: list[str],
    enzymes: list[str],
    data_dir: Path | None = None,
    tmp_dir: Path | None = None,
    *,
    remove_old_cache: bool = True,
) -> pd.DataFrame:
    data_dir = _default_data_dir(data_dir)
    tmp_dir = _default_tmp_dir(tmp_dir, remove_old_cache=remove_old_cache)
    _check_if_data_exists(data_dir)

    df_met = _metabolite_preprocessing(substrates, tmp_dir=tmp_dir, data_dir=data_dir)
    df_met = _calculate_gnn_representations(df_met, tmp_dir=tmp_dir, data_dir=data_dir)
    df_enzyme = _esm1b_vectors(enzymes)

    kms = pd.DataFrame(
        data={
            "substrate": substrates,
            "enzyme": enzymes,
            "index": list(range(len(substrates))),
        },
    )
    kms = _merge_dfs(df_met, df_enzyme, kms)

    valid = kms["complete"]
    kms.loc[valid, "KM [mM]"] = _predict_km(
        _xgb_input_matrix(kms.loc[valid]),
        data_dir=data_dir,
    )

    kms = kms.sort_values(by=["index"])

    return kms.drop(columns=["index"]).reset_index(drop=True)
