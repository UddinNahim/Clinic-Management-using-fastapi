from sqlalchemy.orm import Session
from db.models.doctor import Doctor
from db.models.patient import Patient
from  schemas.auth import RegisterUser, LoginUser
from core.security import hash_password, verify_password, create_access_token

class AuthRepository:
    def __init__(self, db: Session):
        self.db = db

    def register_user(self, user_data: RegisterUser, role: str):
        hashed_pwd = hash_password(user_data.password)
        
        if role == "doctor":
            new_user = Doctor(name=user_data.name, email=user_data.email, hashed_password=hashed_pwd)
        elif role == "patient":
            new_user = Patient(name=user_data.name, email=user_data.email, hashed_password=hashed_pwd)
        else:
            return None
        
        self.db.add(new_user)
        self.db.commit()
        self.db.refresh(new_user)
        return new_user

    def authenticate_user(self, email: str, password: str, role: str):
        if role == "doctor":
            user = self.db.query(Doctor).filter(Doctor.email == email).first()
        else:
            user = self.db.query(Patient).filter(Patient.email == email).first()
        
        if not user or not verify_password(password, user.hashed_password):
            return None
        
        access_token = create_access_token({"sub": user.email, "role": role})
        return access_token
