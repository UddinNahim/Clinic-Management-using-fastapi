from fastapi import HTTPException
from sqlalchemy.orm import Session
from db.models.appointment import Appointment
from schemas.appointment import AppointmentCreate


class AppointmentRepository:
    def __init__(self, db: Session):
        self.db = db

    def create_appointment(self, appointment: AppointmentCreate):
        db_appointment = Appointment(**appointment.dict())
        self.db.add(db_appointment)
        self.db.commit()
        self.db.refresh(db_appointment)
        return db_appointment

    def get_appointments(self):
        return self.db.query(Appointment).all()

    def get_appointment_by_id(self, appointment_id: int):
        return self.db.query(Appointment).filter(Appointment.id == appointment_id).first()
    
    def update_appointment(self, appointment_id:int,update_data:dict):
        appointment = self.get_appointment_by_id(appointment_id)
        if appointment:
            for key, value in update_data.items():
                setattr(appointment,key,value)
            self.db.commit()
            self.db.refresh(appointment)
        return appointment
    
    def delete_appointment(self, appointment_id:int):
        appointment = self.get_appointment_by_id(appointment_id)
        if appointment:
            self.db.delete(appointment)
            self.db.commit()
        return appointment

