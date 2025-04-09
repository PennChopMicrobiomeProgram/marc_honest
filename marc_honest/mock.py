from marc_honest.db import get_session
from marc_honest.models import Subject, Specimen
from sqlalchemy.orm import Session

subject1 = Subject(subject_id=1, mrn="123")
subject2 = Subject(subject_id=2, mrn="456")
specimen1 = Specimen(specimen_id=1, specimen_barcode="SA")
specimen2 = Specimen(specimen_id=2, specimen_barcode="SB")


def fill_mock_db(session: Session = get_session()):
    # Check that db is an empty test db
    assert (
        len(session.query(Subject).all()) == 0
    ), "Database is not empty, I can only add test data to an empty database"

    session.add_all([subject1, subject2, specimen1, specimen2])
    session.commit()
