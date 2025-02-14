from sqlalchemy.orm import Session
from db.models.doctor import Doctor
from schemas.doctor import DoctorCreate



def create_doctor(db: Session, doctor: DoctorCreate):
    db_doctor = Doctor(**doctor.dict())
    db.add(db_doctor)
    db.commit()
    db.refresh(db_doctor)
    return db_doctor

def get_doctors(db: Session):
    return db.query(Doctor).all()

def get_doctor_by_id(db: Session, doctor_id: int):
    return db.query(Doctor).filter(Doctor.id == doctor_id).first()
