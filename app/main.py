from fastapi import FastAPI
from app.routers import webhook
app = FastAPI(title= "Curso de ChatBot Academy")

app.include_router(webhook.router)