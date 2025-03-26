from sqlalchemy import Column, Integer, Text, Date, ForeignKey
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class Subject(Base):
    __tablename__ = "subjects"

    subject_id = Column(Integer, primary_key=True)
    mrn = Column(Text, nullable=False, unique=True)  # PHI


class Specimen(Base):
    __tablename__ = "specimens"

    specimen_id = Column(Integer, primary_key=True)
    specimen_barcode = Column(Text, nullable=False, unique=True)  # PHI
