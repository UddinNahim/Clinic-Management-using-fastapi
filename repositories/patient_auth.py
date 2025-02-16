from typing import Optional
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from db.session import get_db
from utils.password_manager import PasswordManager
from db.models.patient import Patient  # Ensure Patient model is imported
from utils.jwt_manager import verify_token  # Ensure this function exists and is imported

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/patients/token")

def get_patient_by_id(db: Session, id: int) -> Optional[Patient]:
    """Fetch a patient by their ID."""
    return db.query(Patient).filter(Patient.id == id).first()

def get_patient_for_token(db: Session, email: str, password: str) -> Optional[Patient]:
    """Authenticate patient by email and password."""
    patient = db.query(Patient).filter(Patient.email == email).first()
    if not patient:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    is_password_matched = PasswordManager.verify_password(password, patient.password)
    if not is_password_matched:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    return patient

def get_current_patient(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    """Extract and return the current patient from the token."""
    payload = verify_token(token)
    if payload is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
    
    patient = db.query(Patient).filter(Patient.id == payload.get("sub")).first()
    if patient is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Patient not found")
    
    return patient
