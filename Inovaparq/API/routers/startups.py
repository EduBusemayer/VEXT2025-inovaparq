from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from Inovaparq.API.database.db import SessionLocal
from Inovaparq.API.database.models import Startup as StartupModel, createStartupTable
from Inovaparq.API.schemas.startup import Startup, StartupCreate, StartupUpdate

router: APIRouter = APIRouter(prefix = '/startups', tags = ['Startups'])

def getDb():
    try:
        yield SessionLocal()
    finally:
        SessionLocal().close()

@router.post('/', response_model = Startup)
def insertStartup(startup: StartupCreate, db: Session = Depends(getDb)):
    createStartupTable()
    dbStartup = db.query(StartupModel).filter(StartupModel.name == startup.name).first()
    if dbStartup: raise HTTPException(status_code = 400, detail = 'Startup already exists')
    newStartup = StartupModel(**startup.dict())
    db.add(newStartup)
    db.commit()
    db.refresh(newStartup)
    return (newStartup)

@router.get('/{startupId}', response_model = Startup)
def getStartup(startupId: int, db: Session = Depends(getDb)):
    startup = db.query(StartupModel).filter(StartupModel.id == startupId).first()
    if startup: return startup
    raise HTTPException(status_code = 404, detail = 'Startup not found')

@router.get('/listStartups/all', response_model = list[Startup])
def getAllStartups(db: Session = Depends(getDb)):
    startups = db.query(StartupModel).all()
    if startups: return startups
    raise HTTPException(status_code = 404, detail = 'No startups found')

@router.put('/{startupId}', response_model = Startup)
def updateStartup(startupId: int, startupUpdate: StartupUpdate, db: Session = Depends(getDb)):
    startup = db.query(StartupModel).filter(StartupModel.id == startupId).first()
    if not startup: raise HTTPException(status_code = 404, detail = 'Startup not found')
    for key, value in startupUpdate.dict(exclude_unset = True).items(): setattr(startup, key, value)
    db.commit()
    db.refresh(startup)
    return startup

@router.delete('/{startupId}')
def deleteStartup(startupId: int, db: Session = Depends(getDb)):
    startup = db.query(StartupModel).filter(StartupModel.id == startupId).first()
    if not startup: raise HTTPException(status_code = 404, detail = 'Startup not found')
    db.delete(startup)
    db.commit()
    return {"detail": f"Startup '{startup.name}' deleted successfully"}
