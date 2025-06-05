from typing import Literal
from pydantic import BaseModel

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
