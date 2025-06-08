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

@router.post('/')
def login(form_data: LoginRequest, db: Session = Depends(getDb)):
    user = db.query(UserModel).filter(UserModel.email == form_data.email).first()
    if not user or user.password != form_data.password:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    user_data = jsonable_encoder(user)
    user_data.pop("password", None)
    return {"user": user_data}
