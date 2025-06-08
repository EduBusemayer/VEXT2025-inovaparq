from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from Inovaparq.API.database.db import SessionLocal
from fastapi.encoders import jsonable_encoder

from Inovaparq.API.database.models import User as UserModel

def getDb():
    try:
        yield SessionLocal()
    finally:
        SessionLocal().close()

router = APIRouter()

class LoginRequest(BaseModel):
    email: str
    password: str

@router.post('/login')
def login(form_data: LoginRequest, db: Session = Depends(getDb)):
    user = db.query(UserModel).filter(UserModel.email == form_data.email).first()

    if not user or user.password != form_data.password:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    # Converte para dict e remove a senha
    user_data = jsonable_encoder(user)
    user_data.pop("password", None)

    return {"user": user_data}