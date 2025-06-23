from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from Inovaparq.API.database.db import SessionLocal
from Inovaparq.API.database.models import User as UserModel, Startup as StartupModel
from Inovaparq.API.schemas.user import UserCreate, User, UserUpdate

router: APIRouter = APIRouter(prefix = '/users', tags = ['Users'])

def getDb():
    try:
        yield SessionLocal()
    finally:
        SessionLocal().close()

@router.post('/', response_model = User)
def insertUser(user: UserCreate, db: Session = Depends(getDb)):
    dbUser = db.query(UserModel).filter(UserModel.email == user.email).first()
    if dbUser: raise HTTPException(status_code = 400, detail = 'User already exists')
    newUser = UserModel(**user.dict())
    db.add(newUser)
    db.commit()
    db.refresh(newUser)
    return (newUser)

@router.get('/{userId}', response_model = User)
def getUser(userId: int, db: Session = Depends(getDb)):
    user = db.query(UserModel).filter(UserModel.id == userId).first()
    if user: return user
    raise HTTPException(status_code = 404, detail = 'User not found')

@router.get('/', response_model = list[User])
def getAllUsers(db: Session = Depends(getDb)):
    users = db.query(UserModel).all()
    if users: return users
    raise HTTPException(status_code = 404, detail = 'No users found')

@router.put('/{userId}', response_model = User)
def updateUser(userId: int, userUpdate: UserUpdate, db: Session = Depends(getDb)):
    user = db.query(UserModel).filter(UserModel.id == userId).first()
    if not user: raise HTTPException(status_code = 404, detail = 'User not found')
    for key, value in userUpdate.dict(exclude_unset = True).items(): setattr(user, key, value)
    db.commit()
    db.refresh(user)
    return user

@router.delete('/{userId}')
def deleteUser(userId: int, db: Session = Depends(getDb)):
    user = db.query(UserModel).filter(UserModel.id == userId).first()
    if not user: raise HTTPException(status_code = 404, detail = 'User not found')
    db.delete(user)
    db.commit()
    return {"detail": f"User '{user.name}' deleted successfully"}

@router.get('/email/{email}', response_model = User)
def getUserByEmail(email: str, db: Session = Depends(getDb)):
    user = db.query(UserModel).filter(UserModel.email == email).first()
    if user: return user
    raise HTTPException(status_code = 404, detail = 'User not found')

@router.get('/listUsers/{startupId}', response_model = dict)
def getAllUsersByStartup(startupId: int, db: Session = Depends(getDb)):
    dbUsers = db.query(UserModel).filter(UserModel.startup_id == startupId).all()
    dbStartup = db.query(StartupModel).filter(StartupModel.id == startupId).first()
    if not dbStartup: raise HTTPException(status_code = 404, detail = 'Startup not found')
    if not dbUsers: raise HTTPException(status_code = 404, detail = 'No users found')
    return {"users": [{"name": user.name, "email": user.email} for user in dbUsers]}