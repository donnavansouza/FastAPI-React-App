from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from database import base

class Relatorios(base):
    __tablename__ = "relatorios"
    
    id = Column(Integer, primary_key=True, index=True)
    titulo = Column(String)
    relatorio = Column(String)
    autor = Column(String)
    municipio = Column(String)
    ano = Column(String)
