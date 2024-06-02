from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from typing import List, Annotated
import requests
from fastapi import FastAPI, Request, HTTPException, Depends
import models
from sqlalchemy.orm import Session
from database import sessionLocal, engine
import requests
from fastapi.middleware.cors import CORSMiddleware

url = "http://localhost:8000/"

try:
    response = requests.get(url)
    response.raise_for_status()  # Check for HTTP request errors
    data = response.json()  # Parse the JSON response
    print("data exists")
except requests.exceptions.HTTPError as err:
    print(f"HTTP error occurred: {err}")
except Exception as err:
    print(f"Other error occurred: {err}")
    
app = FastAPI()  
  
origins = [
    "http://localhost:3000"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)
    


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
    
def get_year_poverty(ano):
    anos = [1991, 2000, 2010]
    ano_escolhido = anos[0]
    for i in anos:
        if abs(i - int(ano)) < abs(ano_escolhido - int(ano)):
            ano_escolhido = i
    return str(ano_escolhido)

def get_year_population(ano):
    anos = [1991, 2000, 2010, 2014, 2017]
    ano_escolhido = anos[0]
    for i in anos:
        if abs(i - int(ano)) < abs(ano_escolhido - int(ano)):
            ano_escolhido = i
    return str(ano_escolhido)


# app.mount("/static", StaticFiles(directory="static"))

# templates = Jinja2Templates(directory="templates")


# @app.get("/", response_class=HTMLResponse)
# async def read_item(request: Request):
#     return templates.TemplateResponse("index.html", {"request": request})


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
    for item in data:  
        if item['Nome'].lower() == relatorio.municipio.lower():
            populationkey = f"populacao total {get_year_population(relatorio.ano)}"
            povertkey = f"porc de extremamente pobres {get_year_poverty(relatorio.ano)}"
            idhmkey = f"IDHM {get_year_poverty(relatorio.ano)}"
            db_relatorio = models.Relatorios(titulo=relatorio.titulo, relatorio=relatorio.relatorio, autor=relatorio.autor, municipio=item['Nome'], ano=relatorio.ano, populacao=item[populationkey] + " - " + get_year_population(relatorio.ano), porc_extrema_pobreza=item[povertkey] + " - " + get_year_poverty(relatorio.ano), idhm=item[idhmkey] + " - " + get_year_poverty(relatorio.ano))
            db.add(db_relatorio)
            db.commit()
            db.refresh(db_relatorio)
            return db_relatorio
    else:
        raise HTTPException(status_code=404, detail="Municipio not found")


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
    



