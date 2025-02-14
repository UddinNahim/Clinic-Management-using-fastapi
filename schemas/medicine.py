from pydantic import BaseModel

class MedicineBase(BaseModel):
    name:str
    manufacturer:str
    price : float
    stock: int = 0

class MedicineCreate(MedicineBase):
    pass

class MedicineResponse(MedicineBase):
    id:int

    class Config:
        orm_mode = True