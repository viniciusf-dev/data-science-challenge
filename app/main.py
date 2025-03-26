from fastapi import FastAPI
from app.routers import questions

app = FastAPI(title="Order Questions API", version="1.0")


app.include_router(questions.router)
