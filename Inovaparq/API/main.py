from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from API.routers import startups, users

app = FastAPI()
origins = [
    "http://localhost:5173",  # origem do seu frontend
    # você pode adicionar outras URLs se quiser liberar mais frontends
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,       # libera o frontend para fazer requisição
    allow_credentials=True,
    allow_methods=["*"],         # permite todos os métodos (GET, POST, etc)
    allow_headers=["*"],         # permite todos os headers
)

app.include_router(users.router)
app.include_router(startups.router)
'''
@app.get("/")
def default() -> list:
    return [{'Users': users.teste}, {'Startups': startups.teste}]
'''
@app.get("/")
def default():
    return {"message": "API Inovaparq está rodando!"}

