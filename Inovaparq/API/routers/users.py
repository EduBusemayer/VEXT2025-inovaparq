from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from API.database import SessionLocal
from API.models import User as UserModel, ProfileEnum
from API.schemas.user import UserCreate, User, UserUpdate

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

router: APIRouter = APIRouter(prefix='/users', tags=['Users'])

@router.post('/', response_model=User)
def insertUser(user: UserCreate, db: Session = Depends(get_db)):
    db_user = db.query(UserModel).filter(UserModel.email == user.email).first()
    if db_user:
        raise HTTPException(status_code=400, detail='User already exists')
    new_user = UserModel(
        name=user.name,
        email=user.email,
        password=user.password,
        profile=ProfileEnum(user.profile)
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@router.get('/{userId}', response_model=User)
def getUser(userId: int, db: Session = Depends(get_db)):
    user = db.query(UserModel).filter(UserModel.id == userId).first()
    if user:
        return user
    raise HTTPException(status_code=404, detail='User not found')

@router.put('/{userId}', response_model=User)
def updateUser(userId: int, userUpdate: UserUpdate, db: Session = Depends(get_db)):
    user = db.query(UserModel).filter(UserModel.id == userId).first()
    if not user:
        raise HTTPException(status_code=404, detail='User not found')
    for key, value in userUpdate.dict(exclude_unset=True).items():
        setattr(user, key, value)
    db.commit()
    db.refresh(user)
    return user

@router.delete('/{userId}')
def deleteUser(userId: int, db: Session = Depends(get_db)):
    user = db.query(UserModel).filter(UserModel.id == userId).first()
    if not user:
        raise HTTPException(status_code=404, detail='User not found')
    db.delete(user)
    db.commit()
    return {"detail": f"User '{user.name}' deleted successfully"}