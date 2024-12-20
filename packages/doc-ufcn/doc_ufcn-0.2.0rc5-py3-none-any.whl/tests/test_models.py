from pathlib import Path

import pytest
from huggingface_hub.utils import RepositoryNotFoundError, RevisionNotFoundError
from pytest_lazy_fixtures import lf as lazy_fixture

from doc_ufcn import models

BLOB_REFERENCE = "0bdb94c369a902c0f7ffa864d744afa00128308c"


@pytest.mark.parametrize(
    ("name", "version", "expected_model_path", "expected_parameters", "correct_name"),
    [
        # Correct name and version
        (
            "Teklia/doc-ufcn-generic-page",
            "main",
            (
                Path("~/.cache")
                / "doc-ufcn"
                / "models"
                / "Teklia"
                / "doc-ufcn-generic-page"
                / "models--Teklia--doc-ufcn-generic-page"
                / "snapshots"
                / BLOB_REFERENCE
            ),
            lazy_fixture("test_parameters"),
            True,
        ),
        # Correct name and incorrect version
        ("Teklia/doc-ufcn-generic-page", "version", None, None, True),
        # Correct name and no version
        (
            "Teklia/doc-ufcn-generic-page",
            None,
            (
                Path("~/.cache")
                / "doc-ufcn"
                / "models"
                / "Teklia"
                / "doc-ufcn-generic-page"
                / "models--Teklia--doc-ufcn-generic-page"
                / "snapshots"
                / BLOB_REFERENCE
            ),
            lazy_fixture("test_parameters"),
            True,
        ),
        # Incorrect name and incorrect version
        ("page_model", "version", None, None, False),
        # Incorrect name and no version
        ("page_model", None, None, None, False),
    ],
)
def test_download_model(
    name: str,
    version: str | None,
    expected_model_path: Path | None,
    expected_parameters: dict | None,
    correct_name: bool,
):
    """
    Test of the download_model function.
    Check that the correct model is loaded.
    """
    if expected_model_path is None and expected_parameters is None:
        if correct_name:
            # Bad model name
            with pytest.raises(RevisionNotFoundError):
                model_path, parameters = models.download_model(name, version)
        else:
            # Bad revision
            with pytest.raises(RepositoryNotFoundError):
                model_path, parameters = models.download_model(name, version)
    else:
        assert expected_model_path
        model_path, parameters = models.download_model(name, version)
        assert model_path == expected_model_path.expanduser() / "model.pth"
        assert parameters == expected_parameters
