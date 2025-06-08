from sqlalchemy import Column, Integer, String
from Inovaparq.API.database.db import Base

# Deixei separado para caso queira criar as tabelas apenas quando for adicionar um usuário ou startup
'''
def ensure_user_table():
    User.__table__.create(bind = engine, checkfirst = True) 
    
def ensure_startup_table():
    Startup.__table__.create(bind = engine, checkfirst = True)

'''    


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key = True, index = True)
    name = Column(String(50), nullable = False)
    email = Column(String(50), unique = True, index = True, nullable = False)
    password = Column(String(50), nullable = False)
    profile = Column(String(10), nullable = False)
    startup_id = Column(Integer, nullable = True)
    
class Startup(Base):
    __tablename__ = "startups"

    id = Column(Integer, primary_key = True, index = True)
    name = Column(String(50), nullable = False)
    description = Column(String(200), nullable = False)
    incubator = Column(String(10), nullable = False) 
    stage = Column(String(20), nullable = False)
