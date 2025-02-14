from fastapi import APIRouter, Depends
from sqlalchemy.orm  import Session
from db.session import SessionLocal, get_db
from repositories import patient as patient_repo
from schemas.patient import PatientCreate, PatientResponse

router = APIRouter(prefix="/patients", tags=["Patients"])

@router.post("/",response_model=PatientResponse)

def create_patient(patient:PatientCreate,db:Session = Depends(get_db)):
    return patient_repo.create_patient(db,patient)

@router.get("/",response_model=list[PatientResponse])
def get_patients(db:Session = Depends(get_db)):
    return patient_repo.get_patients(db)

@router.get("/{patient_id}",response_model=PatientResponse)
def get_patient(patient_id : int, db:Session = Depends(get_db)):
    return patient_repo.get_patient_by_id(db,patient_id)