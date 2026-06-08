import os
from datetime import datetime
from sqlalchemy import create_engine, Column, Integer, String, Float, Date, Text, DateTime
from sqlalchemy.orm import declarative_base, sessionmaker

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "patients.db")
engine = create_engine(f"sqlite:///{DB_PATH}", echo=False)

Base = declarative_base()
SessionLocal = sessionmaker(bind=engine)


class Patient(Base):
    __tablename__ = "patients"

    id = Column(Integer, primary_key=True, autoincrement=True)
    full_name = Column(String(150), nullable=False)
    dob = Column(Date, nullable=False)
    email = Column(String(200), nullable=False, unique=True)
    glucose = Column(Float, nullable=False)
    haemoglobin = Column(Float, nullable=False)
    cholesterol = Column(Float, nullable=False)
    remarks = Column(Text, nullable=True, default="")
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)


def init_db():
    Base.metadata.create_all(bind=engine)


def get_session():
    return SessionLocal()


def add_patient(full_name, dob, email, glucose, haemoglobin, cholesterol, remarks=""):
    session = get_session()
    try:
        new_patient = Patient(
            full_name=full_name, dob=dob, email=email,
            glucose=glucose, haemoglobin=haemoglobin,
            cholesterol=cholesterol, remarks=remarks,
        )
        session.add(new_patient)
        session.commit()
        session.refresh(new_patient)
        return new_patient.id, None
    except Exception as e:
        session.rollback()
        if "UNIQUE constraint" in str(e):
            return None, "A patient with this email already exists."
        return None, f"Database error: {str(e)}"
    finally:
        session.close()


def get_all_patients():
    session = get_session()
    try:
        patients = session.query(Patient).order_by(Patient.created_at.desc()).all()
        result = []
        for p in patients:
            result.append({
                "id": p.id, "full_name": p.full_name, "dob": p.dob,
                "email": p.email, "glucose": p.glucose,
                "haemoglobin": p.haemoglobin, "cholesterol": p.cholesterol,
                "remarks": p.remarks, "created_at": p.created_at,
            })
        return result
    finally:
        session.close()


def get_patient_by_id(patient_id):
    session = get_session()
    try:
        p = session.query(Patient).filter(Patient.id == patient_id).first()
        if not p:
            return None
        return {
            "id": p.id, "full_name": p.full_name, "dob": p.dob,
            "email": p.email, "glucose": p.glucose,
            "haemoglobin": p.haemoglobin, "cholesterol": p.cholesterol,
            "remarks": p.remarks, "created_at": p.created_at,
        }
    finally:
        session.close()


def email_exists_for_other(email, current_id):
    session = get_session()
    try:
        existing = session.query(Patient).filter(
            Patient.email == email, Patient.id != current_id
        ).first()
        return existing is not None
    finally:
        session.close()


def update_patient(patient_id, full_name, dob, email, glucose, haemoglobin, cholesterol, remarks):
    session = get_session()
    try:
        p = session.query(Patient).filter(Patient.id == patient_id).first()
        if not p:
            return False, "Patient not found."
        p.full_name = full_name
        p.dob = dob
        p.email = email
        p.glucose = glucose
        p.haemoglobin = haemoglobin
        p.cholesterol = cholesterol
        p.remarks = remarks
        p.updated_at = datetime.now()
        session.commit()
        return True, None
    except Exception as e:
        session.rollback()
        return False, str(e)
    finally:
        session.close()


def delete_patient(patient_id):
    session = get_session()
    try:
        p = session.query(Patient).filter(Patient.id == patient_id).first()
        if not p:
            return False, "Patient record not found."
        session.delete(p)
        session.commit()
        return True, None
    except Exception as e:
        session.rollback()
        return False, str(e)
    finally:
        session.close()