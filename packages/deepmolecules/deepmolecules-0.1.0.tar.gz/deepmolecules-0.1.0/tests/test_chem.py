from deepmolecules._chem import (
    _assign_type,
    _is_valid_inchi,
    _is_valid_kegg,
    _is_valid_smiles,
)


def test_assign_type() -> None:
    assert _assign_type("Ethanol") == "invalid"
    assert _assign_type("C00469") == "KEGG"
    assert _assign_type("InChI=1S/C2H6O/c1-2-3/h3H,2H2,1H3") == "InChI"
    assert _assign_type("CCO") == "SMILES"


def test_is_valid_kegg() -> None:
    assert _is_valid_kegg("C00469")
    assert not _is_valid_kegg("Ethanol")


def test_is_valid_smiles() -> None:
    assert _is_valid_smiles("CCO")
    assert not _is_valid_smiles("Ethanol")


def test_is_valid_inchi() -> None:
    assert _is_valid_inchi("InChI=1S/C2H6O/c1-2-3/h3H,2H2,1H3")
    assert not _is_valid_inchi("Ethanol")
