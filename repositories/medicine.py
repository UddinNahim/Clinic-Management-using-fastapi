from sqlalchemy.orm import Session
from db.models.medicine import Medicine
from schemas.medicine import MedicineCreate
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException

class MedicineRepository:
    def __init__(self, db:Session):
        self.db = db
    def create_medicine(self,medicine:MedicineCreate):
        db_medicine = Medicine(**medicine.dict())
        try:
            self.db.add(db_medicine)
            self.db.commit()
            self.db.refresh(db_medicine)
        except IntegrityError as e:
            print(e)
            self.db.rollback()
            raise HTTPException(status_code=400, detail=f"Something went wrong!")
        return db_medicine
    
    def get_medicines(self):
        return self.db.query(Medicine).all()
    
    def get_medicines_by_id(self,medicine_id: int):
        return self.db.query(Medicine).filter(Medicine.id == medicine_id).first()
    
    def update_medicine_stock(self,medicine_id:int, new_stock:int):
        medicine = self.db.query(Medicine).filter(Medicine.id ==medicine_id ).first()
        if medicine:
            medicine.stock = new_stock
            self.db.commit()
            self.db.refresh(medicine)
        return medicine
