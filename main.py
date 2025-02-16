from fastapi import FastAPI
from core.config import settings
from routers import appointment
from routers import doctor
from routers import patient
from routers import medicine
from routers import auth



app = FastAPI(title=settings.PROJECT_NAME,version=settings.PROJECT_VERSION)

app.include_router(doctor.router)
app.include_router(patient.router)
app.include_router(appointment.router)
app.include_router(medicine.router)
app.include_router(auth.router)


# @app.get("/")
# def hello_api():
#         return {"msg":"Hello FastAPI"}