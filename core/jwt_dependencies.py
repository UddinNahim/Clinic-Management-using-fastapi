from fastapi import Depends, HTTPException, Security 
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from core.security import SECRET_KEY,ALGORITHM
from sqlalchemy.orm import Session
from db.session import SessionLocal ,get_db
from db.models.doctor import Doctor
from db.models.patient import Patient


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

def get_current_user(token: str  = Security(oauth2_scheme), db:Session = Depends(get_db)):
    try:
        payload = jwt.decode(token, SECRET_KEY , algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        role:str = payload.get("role")
        if not email or not role:
            raise HTTPException(status_code=401, detail="Invalid token")

        if role == "doctor":
            user = db.query(Doctor).filter(Doctor.email == email).first()
        else:
            user = db.query(Patient).filter(Patient.email == email).first()

        if not user:
            raise HTTPException(status_code=401, detail="User not found")
        return user
    
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")



