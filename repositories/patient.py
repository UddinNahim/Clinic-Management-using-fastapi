from sqlalchemy.orm import Session
from db.models.patient import Patient
from schemas.patient import PatientCreate



class PatientRepository:
    def __init__(self, db: Session):
        self.db = db

    def create_patient(self, patient: PatientCreate):
        db_patient = Patient(**patient.dict())
        self.db.add(db_patient)
        self.db.commit()
        self.db.refresh(db_patient)
        return db_patient

    def get_patients(self):
        return self.db.query(Patient).all()

    def get_patient_by_id(self, patient_id: int):
        return self.db.query(Patient).filter(Patient.id == patient_id).first()

    def update_patient(self, patient_id: int, updated_data: dict):
        patient = self.get_patient_by_id(patient_id)
        if patient:
            for key, value in updated_data.items():
                setattr(patient, key, value)
            self.db.commit()
            self.db.refresh(patient)
        return patient
    
    def delete_patient(self, patient_id:int):
        patient = self.get_patient_by_id(patient_id)
        if patient:
            self.db.delete(patient)
            self.db.commit()
        return patient
