from typing import Literal
from pydantic import BaseModel

class StartupBase(BaseModel):
    name: str
    description: str
    incubator: str
    stage: str
    plan: str

class StartupCreate(StartupBase):
    incubator: Literal['CENTRA', 'CAUSE', 'CRIA-TE', 'NANOTECH']
    stage: Literal['Pré-Incubação', 'Implantação', 'Crescimento', 'Consolidação', 'Graduação']
    plan: Literal['Start', 'Grow']

class StartupUpdate(BaseModel):
    name: str | None = None
    description: str | None = None
    incubator: Literal['CENTRA', 'CAUSE', 'CRIA-TE', 'NANOTECH'] | None = None
    stage: Literal['Pré-Incubação', 'Implantação', 'Crescimento', 'Consolidação', 'Graduação'] | None = None
    plan: Literal['Start', 'Grow']

class Startup(StartupBase):
    id: int
