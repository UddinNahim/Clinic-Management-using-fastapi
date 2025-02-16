from fastapi import APIRouter,Depends, HTTPException
from db.session import get_db
from sqlalchemy.orm import Session
from repositories.auth import AuthRepository
from  schemas.auth import RegisterUser, LoginUser

router = APIRouter()

@router.post("/register{role}")
def register_user(role:str , user_data:RegisterUser, db:Session = Depends(get_db) ):
    if role not in ["doctor", "patient"]:
        raise HTTPException(status_code=400, detail="Invalid role.Choose 'doctor' or 'patient'.")
    repo = AuthRepository(db)
    user = repo.register_user(user_data,role)

    if not user:
        raise HTTPException(status_code=400, detail="User registration failed")
    return {"message":"User registered successfully"}

@router.post("/login")
def login(user_data: LoginUser, role:str, db:Session = Depends(get_db)):
    if role not in ["doctor","patient"]:
        raise HTTPException(status_code=400, detail="Invalid role.choose doctor or patient.")
    repo =AuthRepository(db)
    token = repo.authenticate_user(user_data.email,user_data.password , role)

    if not token:
        raise HTTPException(status_code=401, detail="Invalid Credentials")
    return {"access token": token,"token_type":"bearer"}



