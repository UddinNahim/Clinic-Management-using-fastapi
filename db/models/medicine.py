from sqlalchemy import Column,Integer,Index,String,Float

from db.base_class import Base 



class Medicine(Base):
    __tablename__ = "Medicines"

    id = Column(Integer, primary_key=True,index=True)
    name = Column(String,nullable=False,unique=True)
    manufacturer = Column(String,nullable=False)
    price = Column(Float,nullable=False)
    stock = Column(Integer,nullable=False,default=0)
    