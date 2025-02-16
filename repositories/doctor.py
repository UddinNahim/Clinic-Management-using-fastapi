from sqlalchemy.orm import Session
from db.models.doctor import Doctor
from schemas.doctor import DoctorCreate
from core.security import hash_password

class DoctorRepository:
    def __init__(self, db: Session):
        self.db = db

    def create_doctor(self, doctor: DoctorCreate):
        if not doctor.email:  # Prevent null email
            raise ValueError("Email is required")

        hashed_password = hash_password(doctor.password)

        db_doctor = Doctor(
            name=doctor.name,
            specialty=doctor.specialty,
            phone=doctor.phone,
            email=doctor.email,
            hashed_password=hashed_password
        )

        self.db.add(db_doctor)
        self.db.commit()
        self.db.refresh(db_doctor)
        return db_doctor


    def get_doctors(self):
        return self.db.query(Doctor).all()

    def get_doctor_by_id(self, doctor_id: int):
        return self.db.query(Doctor).filter(Doctor.id == doctor_id).first()
    
    def update_doctor(self, doctor_id:int,update_data: dict):
        doctor = self.get_doctor_by_id(doctor_id)
        if doctor:
            for key, value in update_data.items():
                setattr(doctor,key,value)
            self.db.commit()
            self.db.refresh(doctor)
        return doctor
    
    def delete_doctor(self, doctor_id:int):
        doctor = self.get_doctor_by_id(doctor_id=doctor_id)
        if doctor:
            self.db.delete(doctor)
            self.db.commit()
        return doctor
