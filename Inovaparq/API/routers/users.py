from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from Inovaparq.API.database.db import SessionLocal
from Inovaparq.API.database.models import User as UserModel, Startup as StartupModel, createUserTable
from Inovaparq.API.schemas.user import UserCreate, User, UserUpdate

router: APIRouter = APIRouter(prefix = '/users', tags = ['Users'])

def getDb():
    try:
        yield SessionLocal()
    finally:
        SessionLocal().close()

@router.post('/', response_model = User)
def insertUser(user: UserCreate, db: Session = Depends(getDb)):
    createUserTable() 
    dbUser = db.query(UserModel).filter(UserModel.email == user.email).first()
    dbStartup = db.query(StartupModel).filter(StartupModel.name == user.startupName).first()
    if dbUser: raise HTTPException(status_code = 400, detail = 'User already exists')
    elif not user.startupName and user.profile == 'startup': raise HTTPException(status_code = 400, detail = 'Startup name is required')
    elif user.profile == 'startup' and not dbStartup: raise HTTPException(status_code = 404, detail = 'Startup not found')
    elif user.profile == 'admin' and user.startupName: raise HTTPException(status_code = 400, detail = 'Admin profile cannot have a Startup Name')
    newUser = UserModel(**user.dict(exclude = {'startupName'}), startupId = dbStartup.id if dbStartup else None)
    db.add(newUser)
    db.commit()
    db.refresh(newUser)
    return (newUser)

@router.get('/{userId}', response_model = User)
def getUser(userId: int, db: Session = Depends(getDb)):
    dbUser = db.query(UserModel).filter(UserModel.id == userId).first()
    if dbUser: return dbUser
    raise HTTPException(status_code = 404, detail = 'User not found')

@router.get('/listUsers/all', response_model = list)
def getAllUsers(db: Session = Depends(getDb)):
    data: list = []
    i: int = 0
    dbStartup = db.query(StartupModel).all()
    if not dbStartup: raise HTTPException(status_code = 404, detail = 'No Startups found')
    while i < len(dbStartup):
        dbUsers = db.query(UserModel).filter(UserModel.startupId == dbStartup[i].id).all()
        if not dbUsers: i += 1
        else:
            data.append({dbStartup[i].name: [dbUser.name for dbUser in dbUsers]})
            i += 1
    dbUsers = db.query(UserModel).filter(UserModel.startupId == None).all()
    data.append({'Admins': [dbUser.name for dbUser in dbUsers]})
    return data

@router.get('/listUsers/admins', response_model = dict)
def getAllUsers(db: Session = Depends(getDb)):
    dbUsers = db.query(UserModel).filter(UserModel.startupId == None).all()
    return {'Admins': [dbUser.name for dbUser in dbUsers]}
    
@router.get('/listUsers/{startupId}', response_model = dict)
def getAllUsersByStartup(startupId: int, db: Session = Depends(getDb)):
    dbUsers = db.query(UserModel).filter(UserModel.startupId == startupId).all()
    dbStartup = db.query(StartupModel).filter(StartupModel.id == startupId).first()
    if not dbStartup: raise HTTPException(status_code = 404, detail = 'Startup not found')
    if not dbUsers: raise HTTPException(status_code = 404, detail = 'No users found')
    return {dbStartup.name: [dbUser.name for dbUser in dbUsers]}

@router.put('/{userId}', response_model = User)
def updateUser(userId: int, userUpdate: UserUpdate, db: Session = Depends(getDb)):
    dbUser = db.query(UserModel).filter(UserModel.id == userId).first()
    dbStartup = db.query(StartupModel).filter(StartupModel.name == userUpdate.startupName).first()
    if not dbUser: raise HTTPException(status_code = 404, detail = 'User not found')
    if userUpdate.startupName:
        if not dbStartup: raise HTTPException(status_code = 404, detail = 'Startup not found')
        elif dbUser.profile == 'admin' and not userUpdate.profile == 'startup': raise HTTPException(status_code = 400, detail = 'Admin profile cannot have a linked Startup Name')
        setattr(dbUser, 'startupId', dbStartup.id)
    else:
        if dbUser.profile == 'admin' and userUpdate.profile == 'startup': raise HTTPException(status_code = 400, detail = 'Startup Name is required for startup profile')
        if dbUser.profile == 'startup' and userUpdate.profile == 'admin': setattr(dbUser, 'startupId', None)
    for key, value in userUpdate.dict(exclude_unset = True, exclude = {'startupName'}).items(): setattr(dbUser, key, value)
    db.commit()
    db.refresh(dbUser)
    return dbUser

@router.delete('/{userId}')
def deleteUser(userId: int, db: Session = Depends(getDb)):
    dbUser = db.query(UserModel).filter(UserModel.id == userId).first()
    if not dbUser: raise HTTPException(status_code = 404, detail = 'User not found')
    db.delete(dbUser)
    db.commit()
    return {"detail": f"User '{dbUser.name}' deleted successfully"}

@router.get('/email/{email}', response_model = User)
def getUserByEmail(email: str, db: Session = Depends(getDb)):
    dbUser = db.query(UserModel).filter(UserModel.email == email).first()
    if dbUser: return dbUser
    raise HTTPException(status_code = 404, detail = 'User not found')
