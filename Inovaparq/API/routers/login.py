from fastapi import APIRouter, Depends, HTTPException
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session
from Inovaparq.API.database.db import SessionLocal
from Inovaparq.API.database.models import User as UserModel
from Inovaparq.API.schemas.login import LoginRequest

router: APIRouter = APIRouter(prefix = '/login', tags = ['Startups'])

def getDb():
    try:
        yield SessionLocal()
    finally:
        SessionLocal().close()

@router.post('/', response_model = dict)
def login(formData: LoginRequest, db: Session = Depends(getDb)):
    dbUser = db.query(UserModel).filter(UserModel.email == formData.email).first()
    if not dbUser or dbUser.password != formData.password: raise HTTPException(status_code = 401, detail = 'Invalid credentials')
    userData = jsonable_encoder(dbUser)
    return {'user': userData.pop('password', None)}
