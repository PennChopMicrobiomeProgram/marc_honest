# marc_honest

The honest broker for mARC. Built using SQLAlchemy and Pandas.

## Usage

```
pip install .
export MARC_HONEST_URL="sqlite:////path/to/db.sqlite"
marc_honest -h
marc_honest init
marc_honest broker input.xlsx
```

This will create a database at `/path/to/db.sqlite` then ingest `input.xlsx` and produce `input_anonymized.tsv` which can be fed into marc_db. The `marc_honest broker ...` command is idempotent, meaning you can run it as many times as you want on the same file, it will only ever create one entry for each unique specimen and subject.

## Dev

Use `marc_honest mock` to fill in some test values.