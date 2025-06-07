from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from Inovaparq.API.database.db import Base, engine
from Inovaparq.API.routers import startups, users, login

Base.metadata.create_all(bind = engine)

app = FastAPI()
origins = [
    "http://localhost:5173"
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(users.router)
app.include_router(startups.router)
app.include_router(login.router)

@app.get("/")
def default():
    return {"message": "API Inovaparq está rodando!"}
