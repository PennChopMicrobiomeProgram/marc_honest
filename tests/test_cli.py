import os
import pandas as pd
import pytest
import subprocess as sp
from marc_honest import __version__
from pathlib import Path
from typing import Generator


@pytest.fixture
def db(monkeypatch) -> Generator[str, None, None]:
    """
    Pytest fixture to set up an in-memory SQLite database for testing.
    """
    db_fp = Path(__file__).parent / "test.db"
    db_url = f"sqlite:///{db_fp.resolve()}"
    monkeypatch.setenv("MARC_HONEST_URL", db_url)
    sp.run(["marc_honest", "init"], check=True)

    yield db_url

    db_fp.unlink()


def test_main_version():
    assert (
        __version__
        in sp.run(["marc_honest", "--version"], capture_output=True, text=True).stdout
    )


def test_main(db):
    output_fp = Path(__file__).parent / "test.tsv"
    sp.run(
        [
            "marc_honest",
            "broker",
            str(Path(__file__).parent / "test.xlsx"),
            "--output",
            str(output_fp),
        ],
        check=True,
    )

    assert output_fp.exists()
    df = pd.read_csv(output_fp, sep="\t")
    assert df["Subject ID"].notna().all()
    assert df["Specimen ID"].notna().all()

    sp.run(
        [
            "marc_honest",
            "broker",
            str(Path(__file__).parent / "test.xlsx"),
            "--output",
            str(output_fp),
        ],
        check=True,
    )

    assert output_fp.exists()
    df2 = pd.read_csv(output_fp, sep="\t")
    assert df.equals(df2)

    output_fp.unlink()
