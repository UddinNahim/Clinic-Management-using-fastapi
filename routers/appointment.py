from fastapi import APIRouter, Depends,HTTPException
from sqlalchemy.orm import Session
from db.session import SessionLocal, get_db
from repositories.appointment import AppointmentRepository
from schemas.appointment import AppointmentCreate, AppointmentResponse

router = APIRouter(prefix="/appointments", tags=["Appointments"])



@router.post("/", response_model=AppointmentResponse)
def create_appointment(appointment: AppointmentCreate, db: Session = Depends(get_db)):
    repo = AppointmentRepository(db)
    return repo.create_appointment(appointment)

@router.get("/", response_model=list[AppointmentResponse])
def get_appointments(db: Session = Depends(get_db)):
    repo = AppointmentRepository(db)
    return repo.get_appointments()

@router.get("/{appointment_id}", response_model=AppointmentResponse)
def get_appointment(appointment_id: int, db: Session = Depends(get_db)):
    repo = AppointmentRepository(db)
    return repo.get_appointment_by_id(appointment_id)

@router.put("/{appointment_id}",response_model= AppointmentResponse)
def update_appointment(appointment_id:int,updated_data: dict, db:Session = Depends(get_db)):
    repo = AppointmentRepository(db)
    appointment = repo.update_appointment(appointment_id,updated_data)
    if not updated_data:
        raise HTTPException(status_code=404,detail="appointment not found")
    return appointment

@router.delete("/{appointment_id}")
def delete_appointment(appointment_id:int,db:Session = Depends(get_db)):
    repo = AppointmentRepository(db)
    appointment  = repo.delete_appointment(appointment_id)
    if not appointment:            
            raise HTTPException(status_code=404, detail="appointment not found")
    return {"message":"appontment deleted"}



