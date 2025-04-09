import argparse
import pandas as pd
from pathlib import Path
from marc_honest.db import get_marc_honest_url, get_session
from marc_honest.models import Subject, Specimen
from sqlalchemy.orm import Session


def ingest(input_fp: Path) -> pd.DataFrame:
    df = pd.read_excel(input_fp)

    # Identify tube and box columns
    tube_columns = [col for col in df.columns if col.startswith("Tube Barcode")]
    box_columns = [col for col in df.columns if col.startswith("Box-name_position")]

    # Dynamically determine metadata columns (everything that is NOT a tube or box column)
    metadata_columns = [
        col for col in df.columns if col not in tube_columns + box_columns
    ]

    # Melt the DataFrame to have one row per tube/box (only for existing tube columns)
    df_long = df.melt(
        id_vars=metadata_columns,
        value_vars=tube_columns,
        var_name="Tube Type",
        value_name="Tube Barcode",
    )

    # Extract the tube type (a, b, or c)
    df_long["Tube Type"] = df_long["Tube Type"].str.replace(
        "Tube Barcode ", "", regex=False
    )

    # Melt the box-name-position columns as well (only for existing box columns)
    df_boxes = df.melt(
        id_vars=metadata_columns,
        value_vars=box_columns,
        var_name="Box Type",
        value_name="Box-name_position",
    )

    # Extract the corresponding box type (a, b, or c)
    df_boxes["Box Type"] = df_boxes["Box Type"].str.replace(
        "Box-name_position ", "", regex=False
    )

    # Merge the two melted dataframes on sample metadata and matching Tube/Box types
    df_merged = pd.merge(
        df_long,
        df_boxes,
        left_on=metadata_columns + ["Tube Type"],
        right_on=metadata_columns + ["Box Type"],
        how="left",
    )

    # Drop redundant column
    df_merged.drop(columns=["Box Type"], inplace=True)

    # Remove rows where Tube Barcode is NaN (i.e., no actual tube in that slot)
    df_merged = df_merged.dropna(subset=["Tube Barcode"]).reset_index(drop=True)

    return df_merged


def load(df: pd.DataFrame, session: Session) -> pd.DataFrame:
    for i, r in df.iterrows():
        specimen_barcode = r["Specimen Barcode"]
        mrn = r["MRN"]

        if not session.query(Subject).filter(Subject.mrn == mrn).first():
            subject = Subject(mrn=mrn)
            session.add(subject)
        subject_id = int(
            session.query(Subject).filter(Subject.mrn == mrn).first().subject_id
        )

        if (
            not session.query(Specimen)
            .filter(Specimen.specimen_barcode == specimen_barcode)
            .first()
        ):
            specimen = Specimen(specimen_barcode=specimen_barcode)
            session.add(specimen)
        specimen_id = int(
            session.query(Specimen)
            .filter(Specimen.specimen_barcode == specimen_barcode)
            .first()
            .specimen_id
        )

        df.loc[i, "Subject ID"] = subject_id
        df.loc[i, "Specimen ID"] = specimen_id

    session.commit()
    df.drop(columns=["MRN", "Specimen Barcode"], inplace=True)
    return df


def main(argv: list[str]):
    parser = argparse.ArgumentParser(description="Honest broker for mARC.")
    parser.add_argument("input", help="The input file.")
    parser.add_argument("--output", default="", help="The output file.")
    args = parser.parse_args(argv)

    input_fp = Path(args.input)
    output_fp = Path(args.output)

    if not args.output:
        output_fp = input_fp.parent / f"{input_fp.name}_anonymized.tsv"
    else:
        output_fp = Path(args.output)

    session = get_session()

    df = ingest(input_fp)
    anonymized_df = load(df, session)
    anonymized_df.to_csv(output_fp, sep="\t", index=False)
    print(f"Anonymized data saved to {output_fp}")
