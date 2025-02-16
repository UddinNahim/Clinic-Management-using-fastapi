from pydantic import BaseModel, EmailStr
from datetime import date

class PatientBase(BaseModel):
    name: str
    age: int
    gender: str
    phone: str
    address: str | None = None
    dob: date | None = None
    email: EmailStr
    password: str

class PatientCreate(PatientBase):
    pass  # Used when creating a patient

class PatientResponse(PatientBase):
    id: int
    
class Token(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"

    class Config:
        orm_mode = True
