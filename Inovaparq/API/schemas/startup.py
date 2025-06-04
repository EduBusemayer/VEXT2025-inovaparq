from pydantic import BaseModel

class StartupBase(BaseModel):
    name: str
    description: str
    incubator: str

class StartupCreate(StartupBase):
    incubator: str
    stage: str

class StartupUpdate(BaseModel):
    name: str | None = None
    description: str | None = None
    incubator: str | None = None
    stage: str | None = None

class Startup(StartupBase):
    id: int

    class Config:
        orm_mode = True
        
'''
class StartupBase(BaseModel):
    name: str
    description: str

class StartupCreate(StartupBase):
    incubator: Literal['CENTRA', 'CAUSE', 'CRIA-TE', 'NANOTECH']
    stage: Literal['Pré-Incubação', 'Implantação', 'Crescimento', 'Consolidação', 'Graduação']

class StartupUpdate(BaseModel):
    name: str | None = None
    description: str | None = None
    incubator: Literal['CENTRA', 'CAUSE', 'CRIA-TE', 'NANOTECH'] | None = None
    stage: Literal['Pré-Incubação', 'Implantação', 'Crescimento', 'Consolidação', 'Graduação'] | None = None

class Startup(StartupBase):
    id: int

'''