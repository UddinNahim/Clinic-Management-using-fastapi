from sqlalchemy import Column, Integer, String, ForeignKey ,Date
from sqlalchemy.orm import relationship
from db.base_class import Base
from db.models.appointment import Appointment

class Patient(Base):
    __tablename__ = "patients"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    age = Column(Integer, nullable=False)
    gender = Column(String, nullable=False)
    phone = Column(String, unique=True, nullable=False)
    address = Column(String, nullable=True)
    dob = Column(Date, nullable=True)
    email = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=True)

    # Relationship with Appointments
    appointments = relationship("Appointment", back_populates="patient")
