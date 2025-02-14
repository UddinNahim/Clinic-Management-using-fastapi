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
