from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from API.database import SessionLocal
from API.models import Startup as StartupModel
from API.schemas.startup import Startup, StartupCreate, StartupUpdate

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

router: APIRouter = APIRouter(prefix='/startups', tags=['Startups'])

@router.post('/', response_model=Startup)
def insertStartup(startup: StartupCreate, db: Session = Depends(get_db)):
    db_startup = db.query(StartupModel).filter(StartupModel.name == startup.name).first()
    if db_startup:
        raise HTTPException(status_code=400, detail='Startup already exists')
    new_startup = StartupModel(**startup.dict())
    db.add(new_startup)
    db.commit()
    db.refresh(new_startup)
    return new_startup

@router.get('/{startupId}', response_model=Startup)
def getStartup(startupId: int, db: Session = Depends(get_db)):
    startup = db.query(StartupModel).filter(StartupModel.id == startupId).first()
    if startup:
        return startup
    raise HTTPException(status_code=404, detail='Startup not found')

@router.put('/{startupId}', response_model=Startup)
def updateStartup(startupId: int, startupUpdate: StartupUpdate, db: Session = Depends(get_db)):
    startup = db.query(StartupModel).filter(StartupModel.id == startupId).first()
    if not startup:
        raise HTTPException(status_code=404, detail='Startup not found')
    for key, value in startupUpdate.dict(exclude_unset=True).items():
        setattr(startup, key, value)
    db.commit()
    db.refresh(startup)
    return startup

@router.delete('/{startupId}')
def deleteStartup(startupId: int, db: Session = Depends(get_db)):
    startup = db.query(StartupModel).filter(StartupModel.id == startupId).first()
    if not startup:
        raise HTTPException(status_code=404, detail='Startup not found')
    db.delete(startup)
    db.commit()
    return {"detail": f"Startup '{startup.name}' deleted successfully"}