from fastapi import FastAPI
from API.routers import startups, users

app = FastAPI()
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

