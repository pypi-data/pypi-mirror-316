def test_import() -> None:
    import deepmolecules  # noqa: F401
    from deepmolecules import download_data, kcat, km  # noqa: F401

    assert True
