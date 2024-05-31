from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from typing import List, Annotated
import requests
from fastapi import FastAPI, Request, HTTPException, Depends
import models
from sqlalchemy.orm import Session
from database import sessionLocal, engine

municipios_url = "https://servicodados.ibge.gov.br/api/v1/localidades/estados/23/municipios"

app = FastAPI()

models.base.metadata.create_all(bind=engine)

def get_db():
    db = sessionLocal()
    try:
        yield db
    finally:
        db.close()
        
db_dependency = Annotated[Session,Depends(get_db)]

class Relatorio_model(BaseModel):
    titulo: str
    relatorio: str
    autor: str
    municipio: str
    ano: str
    
    
@app.get("/")
async def root(request: Request):
    return {"message": "Hello World"}


@app.get("/relatorios")
async def get_relatorios(db: db_dependency):
    result = db.query(models.Relatorios).all()
    if not result:
        raise HTTPException(status_code=404, detail="Relatorios not found")
    return result


@app.get("/relatorios/{relatorio_id}")
async def get_relatorio_by_id(relatorio_id: int, db: db_dependency):
    result = db.query(models.Relatorios).filter(models.Relatorios.id == relatorio_id).first()
    if not result:
        raise HTTPException(status_code=404, detail="Relatorio not found")
    return result
    

@app.post("/relatorios")
async def create_relatorio(relatorio: Relatorio_model, db: db_dependency):
    db_relatorio = models.Relatorios(titulo=relatorio.titulo, relatorio=relatorio.relatorio, autor=relatorio.autor, municipio=relatorio.municipio, ano=relatorio.ano)
    db.add(db_relatorio)
    db.commit()
    db.refresh(db_relatorio)


@app.put("/relatorios/{relatorio_id}")
async def update_relatorio(relatorio_id: int, relatorio: Relatorio_model, db: db_dependency):
    db.query(models.Relatorios).filter(models.Relatorios.id == relatorio_id).update(relatorio.dict())
    db.commit()
    in_db_novo_relatorio = db.query(models.Relatorios).filter(models.Relatorios.id == relatorio_id).first()
    return in_db_novo_relatorio
    

@app.delete("/relatorios/{relatorio_id}")
async def delete_relatorio(relatorio_id: int, db: db_dependency):
    relatorio_to_be_deleted = db.query(models.Relatorios).filter(models.Relatorios.id == relatorio_id).delete()
    db.commit()
    return {"message": "Relatorio deleted successfully"}
    



