from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from database import base

class Reports(base):
    __tablename__ = "reports"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    report = Column(String)
    author = Column(String)
    municipality = Column(String)
    year = Column(String)
    population = Column(String)
    extreme_poverty_percentage = Column(String)
    idhm = Column(String)
    bugdet = Column(String)
