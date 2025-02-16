from typing import Optional
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from db.session import get_db
from utils.password_manager import PasswordManager
from db.models.patient import Patient
from utils.jwt_manager import verify_token
from sqlalchemy.exc import IntegrityError


# OAuth2 Scheme
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/patients/token")

class PatientRepository:
    def __init__(self, db: Session):
        self.db = db

    def create_patient(self, patient: Patient):
            # Validate email
            if not patient.email:
                raise HTTPException(status_code=400, detail="Email is required")
            
            # Hash password if provided
            if patient.password:
                hashed_password = PasswordManager.get_password_hash(patient.password)
                patient.password = hashed_password
            
            db_patient = Patient(**patient.dict())
            self.db.add(db_patient)

            try:
                self.db.commit()
                self.db.refresh(db_patient)
            except IntegrityError:
                self.db.rollback()
                raise HTTPException(status_code=400, detail="Email or Phone already registered")
            
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
    
    def delete_patient(self, patient_id: int):
        patient = self.get_patient_by_id(patient_id)
        if patient:
            self.db.delete(patient)
            self.db.commit()
        return patient

    def get_patient_for_token(self, email: str, password: str) -> Optional[Patient]:
        """Authenticate patient by email and password."""
        patient = self.db.query(Patient).filter(Patient.email == email).first()
        if not patient:
            raise HTTPException(status_code=401, detail="Invalid credentials")
        
        is_password_matched = PasswordManager.verify_password(password, patient.password)
        if not is_password_matched:
            raise HTTPException(status_code=401, detail="Invalid credentials")
        
        return patient

    def get_current_patient(self, token: str = Depends(oauth2_scheme)) -> Optional[Patient]:
        """Extract and return the current patient from the token."""
        payload = verify_token(token)
        if payload is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
        
        patient = self.db.query(Patient).filter(Patient.id == payload.get("sub")).first()
        if patient is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Patient not found")
        
        return patient
