from fastapi import HTTPException
from psycopg2 import IntegrityError
from sqlalchemy.orm import Session
from db.models.doctor import Doctor
from schemas.doctor import DoctorCreate
# from core.security import hash_password
from utils.password_manager import PasswordManager

class DoctorRepository:
    def __init__(self, db: Session):
        self.db = db

    def create_doctor(self, doctor: DoctorCreate):
        if not doctor.email:  # Prevent null email
            raise ValueError("Email is required")

        if doctor.password:
                        hashed_password = PasswordManager.get_password_hash(doctor.password)
                        doctor.password = hashed_password
                    
        db_doctor = Doctor(**doctor.dict())
        self.db.add(db_doctor)


        try:
                self.db.commit()
                self.db.refresh(db_doctor)
        except IntegrityError:
                self.db.rollback()
                raise HTTPException(status_code=400, detail="Email or Phone already registered")
            
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
