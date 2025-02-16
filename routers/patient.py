from fastapi import APIRouter, Depends ,HTTPException
from sqlalchemy.orm  import Session
from db.models.patient import Patient
from db.session import SessionLocal, get_db
from repositories.patient import PatientRepository
from repositories.patient_auth import get_current_patient
from schemas.patient import PatientCreate, PatientResponse, Token
from fastapi.security import OAuth2PasswordRequestForm

from utils.jwt_manager import create_access_token,create_refresh_token,verify_token

router = APIRouter(prefix="/patients", tags=["Patients"])


@router.post("/", response_model=PatientResponse)
def create_patient(patient: PatientCreate, db: Session = Depends(get_db)):
    repo = PatientRepository(db)
    db_patient = repo.create_patient(patient)
    return PatientResponse(**db_patient.__dict__)  # Convert SQLAlchemy model to Pydantic


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

@router.post("/token", response_model=Token)
async def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)
):
    """Authenticate patient and return access & refresh tokens."""
    patient = PatientRepository(db=db).get_patient_for_token(
        email=form_data.username, password=form_data.password
    )
    if not patient:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    access_token = create_access_token(data={"sub": str(patient.id)})
    refresh_token = create_refresh_token(data={"sub":str(patient.id)})
    return {"access_token": access_token, "refresh_token": refresh_token}  # Ensure this is a dict


@router.post("/refresh", response_model=Token)
async def refresh_access_token(refresh_request: str, db: Session = Depends(get_db)):
    """Validate refresh token and issue new access token."""
    payload = verify_token(refresh_request.refresh_token)
    
    if payload is None:
        raise HTTPException(status_code=401, detail="Invalid refresh token")

    patient_id = payload.get("sub")
    patient = PatientRepository(db=db).get_patient_by_id(id=patient_id)
    
    if patient is None:
        raise HTTPException(status_code=404, detail="Patient not found")

    access_token = create_access_token(data={"sub": str(patient.id)})
    new_refresh_token = create_refresh_token(data={"sub": str(patient.id)})

    return {"access_token": access_token, "refresh_token": new_refresh_token}

@router.get("/protected")
async def protected_route(current_patient: Patient = Depends(get_current_patient)):
    """Protected route that requires authentication."""
    return {"message": f"Hello {current_patient.email}, you are authorized!"}