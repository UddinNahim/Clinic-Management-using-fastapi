from pydantic import BaseModel

class MedicineBase(BaseModel):
    name:str
    manufacurer:str
    price : float
    stock: int = 0

class MedicineCreate(MedicineBase):
    pass

class MedicineResponse(MedicineBase):
    id:int

    class config:
        orm_mode = True