from sqlalchemy import Column, String, Integer
from sqlalchemy.orm import relationship
from models.base_model import BaseModel

class Guardian(BaseModel):
    """Model representing a guardian."""

    __tablename__ = 'guardians'

    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    gender = Column(String(10), nullable=False)
    dob = Column(String(20), nullable=False)
    occupation = Column(String(100), nullable=False)
    child_name = Column(String(100))
    address = Column(String(255))
    phone = Column(String(20))
    email = Column(String(100))

    # Define relationship with Student model
    students = relationship("Student", back_populates="guardian")

    def __init__(self, name, gender, dob, occupation, child_name=None, address=None, phone=None, email=None):
        super().__init__()
        self.name = name
        self.gender = gender
        self.dob = dob
        self.occupation = occupation
        self.child_name = child_name
        self.address = address
        self.phone = phone
        self.email = email