from fastapi import FastAPI
from app.routers import questions
from app.middlewares.error_handler import register_error_handlers

app = FastAPI(title="Order Questions API", version="1.0")

app.include_router(questions.router)


register_error_handlers(app)
