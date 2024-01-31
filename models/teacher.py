from sqlalchemy import Column, String, Integer
from sqlalchemy.orm import relationship
from models.base_model import BaseModel

class Teacher(BaseModel):
    """Model representing a teacher."""

    __tablename__ = 'teachers'

    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    gender = Column(String(10), nullable=False)
    dob = Column(String(20), nullable=False)
    discipline = Column(String(100), nullable=False)
    classroom = Column(String(100), nullable=False)
    phone_number = Column(String(20))
    address = Column(String(255))
    email = Column(String(100))

    # Define relationship with Student model
    students = relationship("Student", back_populates="teacher")

    def __init__(self, name, gender, dob, discipline, classroom, phone_number=None, address=None, email=None):
        super().__init__()
        self.name = name
        self.gender = gender
        self.dob = dob
        self.discipline = discipline
        self.classroom = classroom
        self.phone_number = phone_number
        self.address = address
        self.email = email