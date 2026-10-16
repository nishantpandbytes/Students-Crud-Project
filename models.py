from sqlalchemy import Column, Integer, String, Date
from database import Base

class Student(Base):
    __tablename__ = "students"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    dob = Column(Date, nullable=False)
    contact = Column(String, nullable=False)
    
    course = Column(String, nullable=True)
    address = Column(String, nullable=True)
    enrollment_date = Column(Date, nullable=True)