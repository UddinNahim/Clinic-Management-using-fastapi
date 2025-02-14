from sqlalchemy.orm import Session
from db.models.patient import Patient
from schemas.patient import PatientCreate



def create_patient(db:Session, patient: PatientCreate):
        db_patient = Patient(**patient.dict())
        db.add(db_patient)
        db.commit()
        db.refresh(db_patient)
        return db_patient

def get_patients(db:Session):
        return db.query(Patient).all()

def get_patient_by_id(db:Session, patient_id:int):
        return db.query(Patient).filter(Patient.id == patient_id).first()
