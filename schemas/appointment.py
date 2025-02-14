from pydantic import BaseModel
from datetime import datetime

class AppointmentBase(BaseModel):
    doctor_id: int
    patient_id: int
    appointment_date: datetime
    status: str = "Scheduled"

class AppointmentCreate(AppointmentBase):
    pass  # Used when creating an appointment

class AppointmentResponse(AppointmentBase):
    id: int

    class Config:
        orm_mode = True
