from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.orm import relationship
from models.base_model import BaseModel

class Student(BaseModel):
    """Model representing a student."""

    __tablename__ = 'students'

    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    gender = Column(String(10), nullable=False)
    dob = Column(String(20), nullable=False)
    class_name = Column(String(100), nullable=False)
    height = Column(String(20))
    genotype_blood_group = Column(String(50))
    parent_guardian_id = Column(Integer, ForeignKey('guardians.id'))

    # Define relationship with Guardian model
    guardian = relationship("Guardian", back_populates="students")

    def __init__(self, name, gender, dob, class_name, height=None, genotype_blood_group=None, parent_guardian_id=None):
        super().__init__()
        self.name = name
        self.gender = gender
        self.dob = dob
        self.class_name = class_name
        self.height = height
        self.genotype_blood_group = genotype_blood_group
        self.parent_guardian_id = parent_guardian_id
