from fastapi import FastAPI
from fastapi.testclient import TestClient
from app.middlewares.error_handler import register_error_handlers
from app.exceptions.api_exceptions import APIException

app = FastAPI(debug=False)
register_error_handlers(app)

@app.get("/api_exception")
def raise_api_exception():
    raise APIException("Erro de API", status_code=418)

@app.get("/general_exception")
def raise_general_exception():
    raise Exception("Erro genérico")

client = TestClient(app, raise_server_exceptions=False)

def test_api_exception_handler():
    response = client.get("/api_exception")
    assert response.status_code == 418
    assert response.json() == {"detail": "Erro de API"}

def test_general_exception_handler():
    response = client.get("/general_exception")
    assert response.status_code == 500
    assert response.json() == {"detail": "Ocorreu um erro interno."}
