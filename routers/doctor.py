from fastapi import APIRouter, Depends ,HTTPException
from sqlalchemy.orm import Session
from db.session import SessionLocal, get_db

from repositories.doctor import DoctorRepository
from schemas.doctor import DoctorCreate, DoctorResponse

router = APIRouter(prefix="/doctors", tags=["Doctors"])


@router.post("/", response_model=DoctorResponse)
def create_doctor(doctor: DoctorCreate, db: Session = Depends(get_db)):
    repo = DoctorRepository(db)
    return repo.create_doctor(doctor)

@router.get("/", response_model=list[DoctorResponse])
def get_doctors(db: Session = Depends(get_db)):
    repo = DoctorRepository(db)
    return repo.get_doctors()

@router.get("/{doctor_id}", response_model=DoctorResponse)
def get_doctor(doctor_id: int, db: Session = Depends(get_db)):
    repo = DoctorRepository(db)
    doctor =  repo.get_doctor_by_id(doctor_id)
    if not doctor:
        raise HTTPException(status_code=404, detail="doctor not found")
    return doctor

@router.put("/{doctor_id}",response_model=DoctorResponse)
def update_doctor(doctor_id:int,updated_data : dict, db:Session = Depends(get_db)):
    repo = DoctorRepository(db)
    doctor = repo.update_doctor(doctor_id, updated_data)
    if not doctor:
        raise HTTPException(status_code=404, detail="doctor not found")
    return doctor

@router.delete("/{doctor_id}")
def delete_doctor(doctor_id: int, db:Session = Depends(get_db)):
    repo = DoctorRepository(db)
    doctor = repo.delete_doctor(doctor_id)
    if not doctor:
        raise HTTPException(status_code=404, detail="Doctor not found")
    return {"message":"doctor deleted successfully"}
  


