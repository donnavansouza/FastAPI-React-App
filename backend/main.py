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


app = FastAPI() 



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



class report_model(BaseModel):
    title: str
    report: str
    author: str
    municipality: str
    year: str
    


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/reports")
async def get_reports(db: db_dependency):
    result = db.query(models.Reports).all()
    if not result:
        raise HTTPException(status_code=404, detail="reports not found")
    return result


@app.get("/reports/{report_id}")
async def get_report_by_id(report_id: int, db: db_dependency):
    result = db.query(models.Reports).filter(models.Reports.id == report_id).first()
    if not result:
        raise HTTPException(status_code=404, detail="report not found")
    return result

    
def get_year_poverty(year):
    years = [1991, 2000, 2010]
    chosen_year = years[0]
    for i in years:
        if abs(i - int(year)) < abs(chosen_year - int(year)):
            chosen_year = i
    return str(chosen_year)

def get_year_population(year):
    years = [1991, 2000, 2010, 2014, 2017]
    chosen_year = years[0]
    for i in years:
        if abs(i - int(year)) < abs(chosen_year - int(year)):
            chosen_year = i
    return str(chosen_year)


@app.post("/reports")
async def create_report(report: report_model, db: db_dependency):
    try:
        response = requests.get(f"https://api-dados-abertos.tce.ce.gov.br/municipios?nome_municipio={report.municipality}")
        response.raise_for_status()  # Check for HTTP request errors
        municipality_code_data = response.json() # Parse the JSON response
        response_budget_data = requests.get(f"https://api-dados-abertos.tce.ce.gov.br/dados_orcamentos?codigo_municipio={municipality_code_data['data'][0]['codigo_municipio']}&exercicio_orcamento={report.year}00")
        budget_data = response_budget_data.json()
        budget_key = str(budget_data['data'][0]['valor_total_fixado_orcamento'])
        print(budget_key)
    except requests.exceptions.HTTPError as err:
        print(f"HTTP error occurred: {err}")
    for item in data:  
        if item["Municipality_name"].lower() == report.municipality.lower():
            populationkey = f"Total population {get_year_population(report.year)}"
            povertkey = f"Extreme poverty percentage {get_year_poverty(report.year)}"
            idhmkey = f"IDHM {get_year_poverty(report.year)}"
            db_report = models.Reports(title=report.title, report=report.report, author=report.author, municipality=item['Municipality_name'], year=report.year, population=item[populationkey] + " " + "("+get_year_population(report.year)+")", extreme_poverty_percentage=item[povertkey] + " " + "("+get_year_poverty(report.year)+")", idhm=item[idhmkey] + " " + "("+get_year_poverty(report.year)+")", bugdet=budget_key + " " + "("+ report.year + ")")
            db.add(db_report)
            db.commit()
            db.refresh(db_report)
            return db_report
    else:
        raise HTTPException(status_code=404, detail="municipality not found")


@app.put("/reports/{report_id}")
async def update_report(report_id: int, report: report_model, db: db_dependency):
    db.query(models.Reports).filter(models.Reports.id == report_id).update(report.dict())
    db.commit()
    in_db_novo_report = db.query(models.Reports).filter(models.Reports.id == report_id).first()
    return in_db_novo_report
    

@app.delete("/reports/{report_id}")
async def delete_report(report_id: int, db: db_dependency):
    report_to_be_deleted = db.query(models.Reports).filter(models.Reports.id == report_id).delete()
    db.commit()
    return {"message": "report deleted successfully"}
    



