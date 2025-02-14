from fastapi import APIRouter, Depends ,HTTPException
from sqlalchemy.orm  import Session
from db.session import SessionLocal, get_db
from repositories.patient import PatientRepository
from schemas.patient import PatientCreate, PatientResponse

router = APIRouter(prefix="/patients", tags=["Patients"])

@router.post("/", response_model=PatientResponse)
def create_patient(patient: PatientCreate, db: Session = Depends(get_db)):
    repo = PatientRepository(db)
    return repo.create_patient(patient)

@router.get("/", response_model=list[PatientResponse])
def get_patients(db: Session = Depends(get_db)):
    repo = PatientRepository(db)
    return repo.get_patients()

@router.get("/{patient_id}", response_model=PatientResponse)
def get_patient(patient_id: int, db: Session = Depends(get_db)):
    repo = PatientRepository(db)
    patient = repo.get_patient_by_id(patient_id)
    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")
    return patient

@router.put("/{patient_id}", response_model=PatientResponse)
def update_patient(patient_id: int, updated_data: dict, db: Session = Depends(get_db)):
    repo = PatientRepository(db)
    patient = repo.update_patient(patient_id, updated_data)
    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")
    return patient

@router.delete("/{patient_id}")
def delete_patient(patient_id:int, db:Session = Depends(get_db)):
    repo = PatientRepository(db)
    patient = repo.delete_patient(patient_id)
    if not patient:
        raise HTTPException(status_code=404, detail="patient not found")
    return {"Patient deleted Successfully"}

