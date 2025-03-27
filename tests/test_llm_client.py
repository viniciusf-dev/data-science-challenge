import os
import pytest
from importlib import reload

def test_format_answer_with_llm_without_gemini(monkeypatch):
    monkeypatch.setenv("GEMINI_API_KEY", "")
    
    import app.services.llm_client as llm_module
    reload(llm_module)
    LLMClient = llm_module.LLMClient
    
    client = LLMClient()
    result = client.format_answer_with_llm(
        "Qual é a pergunta?",
        {"dummy": "Quais as categorias vendidas em maior quantidade?"}
    )
    
    assert result == str({"dummy": "Quais as categorias vendidas em maior quantidade?"})

def test_generate_additional_questions_without_gemini(monkeypatch):
    monkeypatch.setenv("GEMINI_API_KEY", "")
    import app.services.llm_client as llm_module
    reload(llm_module)
    LLMClient = llm_module.LLMClient
    
    client = LLMClient()
    result = client.generate_additional_questions_with_llm(
        "Pergunta",
        {"dummy": "Quais as categorias vendidas em maior quantidade?"}
    )
    assert result == []
