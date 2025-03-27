import pytest
from fastapi.testclient import TestClient
from app.main import app

import app.services.nlp_intent as nlp_intent_module
from app.routers.questions import analyzer, llm


class DummyAnalyzer:
    def top3_electronics_by_credit(self):
        return [{"subcategory": "Dummy", "count": 1}]

class DummyLLM:
    def format_answer_with_llm(self, question, data_result):
        return f"Answer for {question}"

    def generate_additional_questions_with_llm(self, original_question, data_result):
        return [
            {"question": "Dummy Q1", "answer": "Dummy A1"},
            {"question": "Dummy Q2", "answer": "Dummy A2"},
            {"question": "Dummy Q3", "answer": "Dummy A3"}
        ]

@pytest.fixture(autouse=True)
def patch_dependencies(monkeypatch):
    
    monkeypatch.setattr(nlp_intent_module, "detect_intent", lambda question: "top3_electronics_by_credit")
    
    monkeypatch.setattr("app.routers.questions.analyzer", DummyAnalyzer())
    monkeypatch.setattr("app.routers.questions.llm", DummyLLM())

client = TestClient(app)

def test_ask_question_success():
    response = client.post("/ask", json={"question": "Teste de pergunta"})
    assert response.status_code == 200
    data = response.json()
    assert data["question"] == "Teste de pergunta"
    assert data["answer"] == "Answer for Teste de pergunta"
    assert isinstance(data["generated_questions"], list)
    assert len(data["generated_questions"]) == 3

def test_ask_question_intent_not_recognized(monkeypatch):
    
    monkeypatch.setattr(nlp_intent_module, "detect_intent", lambda question: "")
    response = client.post("/ask", json={"question": "Pergunta sem intenção"})
    assert response.status_code == 400
    data = response.json()
    assert "detail" in data

def test_ask_question_function_not_implemented(monkeypatch):
    
    monkeypatch.setattr(nlp_intent_module, "detect_intent", lambda question: "non_existent_intent")
    response = client.post("/ask", json={"question": "Pergunta com intenção não implementada"})
    assert response.status_code == 501
    data = response.json()
    assert "detail" in data
