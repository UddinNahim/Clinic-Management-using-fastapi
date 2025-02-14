from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from db.session import SessionLocal, get_db
from repositories import doctor as doctor_repo
from schemas.doctor import DoctorCreate, DoctorResponse

router = APIRouter(prefix="/doctors", tags=["Doctors"])



@router.post("/", response_model=DoctorResponse)
def create_doctor(doctor: DoctorCreate, db: Session = Depends(get_db)):
    return doctor_repo.create_doctor(db, doctor)

@router.get("/", response_model=list[DoctorResponse])
def get_doctors(db: Session = Depends(get_db)):
    return doctor_repo.get_doctors(db)

@router.get("/{doctor_id}", response_model=DoctorResponse)
def get_doctor(doctor_id: int, db: Session = Depends(get_db)):
    return doctor_repo.get_doctor_by_id(db, doctor_id)
