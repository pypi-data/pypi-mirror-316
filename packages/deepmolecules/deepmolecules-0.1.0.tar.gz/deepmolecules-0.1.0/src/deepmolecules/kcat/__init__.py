from __future__ import annotations

import pickle
from logging import getLogger
from typing import TYPE_CHECKING, cast

import esm
import numpy as np
import pandas as pd
import torch
import xgboost as xgb
from rdkit.Chem.inchi import MolFromInchi
from rdkit.Chem.rdChemReactions import (
    CreateDifferenceFingerprintForReaction,
    ReactionFromSmarts,
)
from rdkit.Chem.rdmolfiles import MolFromMolFile, MolFromSmiles, MolToSmarts

from deepmolecules._chem import _assign_type
from deepmolecules._shared_paths import _default_data_dir

from ._paths import (
    _esm1b_epoch_file,
    _esm1b_train_test_file,
    _mol_file_dir,
    _xgboost_model_file,
    _xgboost_regression_file,
)

__all__ = ["AA", "predict"]

if TYPE_CHECKING:
    from pathlib import Path

AA: set[str] = set("abcdefghiklmnpqrstxvwyzv".upper())

logger = getLogger("deepmolecules")


def _get_reaction_site_smarts(metabolites: str, data_dir: Path) -> str:
    reaction_site = ""
    for met in metabolites.split(";"):
        met_type = _assign_type(met)

        if met_type == "KEGG":
            smarts: str = MolToSmarts(
                MolFromMolFile(str(_mol_file_dir(data_dir) / f"{met}.mol")),
            )
        elif met_type == "InChI":
            smarts = MolToSmarts(MolFromInchi(met))
        elif met_type == "SMILES":
            smarts = MolToSmarts(MolFromSmiles(met))
        else:
            smarts = "invalid"

        reaction_site = f"{reaction_site}.{smarts}"
    return reaction_site[1:]


def _convert_fp_to_array(difference_fp_dict: dict[int, np.ndarray]) -> np.ndarray:
    fp = np.zeros(2048)
    for k, v in difference_fp_dict.items():
        fp[k] = v
    return fp


def _preprocessing(
    substrates: list[str],
    products: list[str],
    data_dir: Path,
) -> pd.DataFrame:
    # removing duplicated entries and creating a pandas DataFrame with all metabolites
    df_reaction = pd.DataFrame(
        data={
            "substrates": substrates,
            "products": products,
        },
    )
    df_reaction["ID"], df_reaction["reaction_message"] = np.nan, np.nan
    df_reaction["difference_fp"] = ""
    # each metabolite should be either a KEGG ID, InChI string, or a SMILES:
    for ind in df_reaction.index:
        df_reaction["ID"][ind] = "reaction_" + str(ind)
        left_site = _get_reaction_site_smarts(
            cast(str, df_reaction.loc[ind, "substrates"]),
            data_dir,
        )
        right_site = _get_reaction_site_smarts(
            cast(str, df_reaction.loc[ind, "products"]),
            data_dir,
        )
        if (
            pd.isna(left_site)
            or pd.isna(right_site)
            or ("invalid" in left_site or "invalid" in right_site)
        ):
            df_reaction["reaction_message"][ind] = "invalid"
        else:
            rxn_forward = ReactionFromSmarts(left_site + ">>" + right_site)
            difference_fp = CreateDifferenceFingerprintForReaction(
                rxn_forward,
            )
            difference_fp = _convert_fp_to_array(difference_fp.GetNonzeroElements())
            df_reaction["difference_fp"][ind] = difference_fp
            df_reaction["reaction_message"][ind] = "complete"
    return df_reaction


def _validate_enzyme(seq: str) -> bool:
    return not (set(seq.upper()) - AA)


def _preprocess_enzymes(enzymes: list[str]) -> pd.DataFrame:
    df_enzyme = pd.DataFrame(data={"amino acid sequence": list(set(enzymes))})
    df_enzyme["ID"] = ["protein_" + str(ind) for ind in df_enzyme.index]
    # if length of sequence is longer than 1020 amino acids, we crop it:
    df_enzyme["model_input"] = [seq[:1022] for seq in df_enzyme["amino acid sequence"]]
    return df_enzyme


def _calculate_esm1b_ts_vectors(enzymes: list[str], data_dir: Path) -> pd.DataFrame:
    df_enzyme = _preprocess_enzymes(enzymes)

    model, alphabet = esm.pretrained.load_model_and_alphabet_core(
        model_name="esm1b_t33_650M_UR50S",
        model_data=torch.load(
            _xgboost_model_file(data_dir),
            map_location="cpu",
        ),
        regression_data=torch.load(
            _xgboost_regression_file(data_dir),
            map_location="cpu",
        ),
    )

    batch_converter = alphabet.get_batch_converter()

    model.eval()  # FIXME: what is this doing?
    model_dict = torch.load(
        _esm1b_epoch_file(data_dir),
        map_location=torch.device("cpu"),
    )
    model_dict_V2 = {k.split("model.")[-1]: v for k, v in model_dict.items()}

    for key in [
        "module.fc1.weight",
        "module.fc1.bias",
        "module.fc2.weight",
        "module.fc2.bias",
        "module.fc3.weight",
        "module.fc3.bias",
    ]:
        del model_dict_V2[key]
    model.load_state_dict(model_dict_V2)

    df_enzyme["enzyme rep"] = ""

    ind: int
    for ind in df_enzyme.index:
        if _validate_enzyme(seq=cast(str, df_enzyme.loc[ind, "model_input"])):
            _, _, batch_tokens = batch_converter(
                [
                    (
                        df_enzyme.loc[ind, "ID"],
                        df_enzyme.loc[ind, "model_input"],
                    ),
                ],  # type: ignore
            )
            with torch.no_grad():
                results = model(batch_tokens, repr_layers=[33])
            df_enzyme["enzyme rep"][ind] = results["representations"][33][0][0].numpy()
    return df_enzyme


def _predict_kcat(x: np.ndarray, data_dir: Path) -> np.ndarray:
    with _esm1b_train_test_file(data_dir).open("rb") as fp:
        bst = pickle.load(fp)
    return 10 ** bst.predict(xgb.DMatrix(x))


def _calculate_xgb_input_matrix(df: pd.DataFrame) -> np.ndarray:
    fingerprints = np.reshape(np.array(list(df["difference_fp"])), (-1, 2048))
    esm1b = np.reshape(np.array(list(df["enzyme rep"])), (-1, 1280))
    return np.concatenate([fingerprints, esm1b], axis=1)


def _merging_reaction_and_enzyme_df(
    reactions: pd.DataFrame,
    enzymes: pd.DataFrame,
    kcats: pd.DataFrame,
) -> pd.DataFrame:
    kcats["difference_fp"], kcats["enzyme rep"] = "", ""
    kcats["complete"] = True

    for ind in kcats.index:
        diff_fp = next(
            iter(
                reactions["difference_fp"]
                .loc[reactions["substrates"] == kcats["substrates"][ind]]
                .loc[reactions["products"] == kcats["products"][ind]],
            ),
        )
        esm1b_rep = next(
            iter(
                enzymes["enzyme rep"].loc[
                    enzymes["amino acid sequence"] == kcats["enzyme"][ind]
                ],
            ),
        )

        if isinstance(diff_fp, str) and isinstance(esm1b_rep, str):
            kcats["complete"][ind] = False
        else:
            kcats["difference_fp"][ind] = diff_fp
            kcats["enzyme rep"][ind] = esm1b_rep
    return kcats


def predict(
    substrates: list[str],
    products: list[str],
    enzymes: list[str],
    data_dir: Path | None = None,
) -> pd.DataFrame:
    data_dir = _default_data_dir(data_dir)
    df_kcat = _merging_reaction_and_enzyme_df(
        reactions=_preprocessing(
            substrates=substrates,
            products=products,
            data_dir=data_dir,
        ),
        enzymes=_calculate_esm1b_ts_vectors(enzymes=enzymes, data_dir=data_dir),
        kcats=pd.DataFrame(
            data={
                "substrates": substrates,
                "products": products,
                "enzyme": [enzyme.upper() for enzyme in enzymes],
                "index": list(range(len(substrates))),
            },
        ),
    )
    df_kcat_valid, df_kcat_invalid = (
        df_kcat.loc[df_kcat["complete"]],
        df_kcat.loc[~df_kcat["complete"]],
    )
    df_kcat_valid = df_kcat_valid.reset_index(drop=True)
    if len(df_kcat_valid) > 0:
        kcats = _predict_kcat(
            _calculate_xgb_input_matrix(df_kcat_valid),
            data_dir=data_dir,
        )
        df_kcat_valid["kcat [s^(-1)]"] = kcats

    return (
        pd.concat([df_kcat_valid, df_kcat_invalid], ignore_index=True)
        .sort_values(by=["index"])
        .drop(columns=["index"])
        .reset_index(drop=True)
    )
