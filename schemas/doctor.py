from pydantic import BaseModel ,EmailStr

class DoctorBase(BaseModel):
    name: str
    specialty: str
    phone: str
    email: EmailStr 
    password: str

class DoctorCreate(DoctorBase):
    pass  # Used when creating a doctor

class DoctorResponse(DoctorBase):
    id: int

    class Config:
        orm_mode = True
