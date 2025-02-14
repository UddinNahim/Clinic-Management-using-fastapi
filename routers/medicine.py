from fastapi import APIRouter,Depends
from sqlalchemy.orm import Session
from db.session import SessionLocal, get_db
from repositories.medicine import MedicineRepository
from schemas.medicine import MedicineCreate, MedicineResponse

router = APIRouter(prefix="/medicines",tags=["Medicines"])

@router.post("/",response_model=MedicineResponse)
def create_medicine(medicine: MedicineCreate, db: Session = Depends(get_db)):
    repo = MedicineRepository(db)
    return repo.create_medicine(medicine)

@router.get("/", response_model=list[MedicineResponse])
def get_medicines(db: Session = Depends(get_db)):
    repo = MedicineRepository(db)
    return repo.get_medicines()

@router.get("/{medicine_id}",response_model=MedicineResponse)
def get_medicine(medicine_id:int, db:Session = Depends(get_db)):
    repo = MedicineRepository(db)
    return repo.get_medicines_by_id(medicine_id)

@router.put("/{medicine_id}/stock")
def update_medicine_stock(medicine_id:int, new_stock:int,db:Session = Depends(get_db)):
    repo = MedicineRepository(db)
    return repo.update_medicine_stock(medicine_id,new_stock)




