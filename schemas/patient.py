from pydantic import BaseModel
from datetime import date

class PatientBase(BaseModel):
    name: str
    age: int
    gender: str
    phone: str
    address: str | None = None
    dob: date | None = None

class PatientCreate(PatientBase):
    pass  # Used when creating a patient

class PatientResponse(PatientBase):
    id: int

    class Config:
        orm_mode = True
