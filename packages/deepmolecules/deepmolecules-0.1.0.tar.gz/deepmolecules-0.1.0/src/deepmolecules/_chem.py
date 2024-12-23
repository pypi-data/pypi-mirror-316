from __future__ import annotations

import re
from typing import TYPE_CHECKING, Literal

from rdkit.Chem.inchi import MolFromInchi
from rdkit.Chem.rdmolfiles import MolFromMolFile, MolFromSmiles
from rdkit.Chem.rdmolops import (
    SanitizeMol,
)

__all__ = ["RE_KEGG_ID", "ChemType"]

if TYPE_CHECKING:
    from pathlib import Path

    from rdkit.Chem.rdchem import Mol

RE_KEGG_ID = re.compile(r"[CD]\d{5}")
ChemType = Literal["KEGG", "InChI", "SMILES", "invalid"]


def _is_valid_kegg(met: str) -> bool:
    return RE_KEGG_ID.fullmatch(met) is not None


def _is_valid_smiles(met: str) -> bool:
    m = MolFromSmiles(met, sanitize=False)
    if m is None:
        return False

    try:
        SanitizeMol(m)
    except:  # noqa: E722
        return False
    return True


def _is_valid_inchi(met: str) -> bool:
    m: Mol | None = MolFromInchi(met, sanitize=False)
    if m is None:
        return False
    try:
        SanitizeMol(m)
    except:  # noqa: E722
        return False
    return True


def _assign_type(met: str) -> ChemType:
    if _is_valid_kegg(met):
        return "KEGG"
    if _is_valid_inchi(met):
        return "InChI"
    if _is_valid_smiles(met):
        return "SMILES"

    return "invalid"


def _get_mol(met: str, mol_file_dir: Path) -> Mol | None:
    if _is_valid_kegg(met):
        try:
            return MolFromMolFile(str(mol_file_dir / f"{met}.mol"))
        except:  # noqa: E722
            return None
    if _is_valid_inchi(met):
        return MolFromInchi(met)
    if _is_valid_smiles(met):
        return MolFromSmiles(met)
    return None
