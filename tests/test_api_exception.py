import pytest
from app.exceptions.api_exceptions import APIException, IntentNotRecognized, FunctionNotImplemented, LLMServiceError, DataAnalysisError

def test_api_exception():
    ex = APIException("erro", 500)
    assert ex.detail == "erro"
    assert ex.status_code == 500

def test_intent_not_recognized_default():
    ex = IntentNotRecognized()
    assert ex.detail == "Desculpe, não entendi a pergunta ou ela foge do escopo."
    assert ex.status_code == 400

def test_function_not_implemented_default():
    ex = FunctionNotImplemented()
    assert ex.detail == "Função não implementada para a intenção detectada."
    assert ex.status_code == 501

def test_llm_service_error_default():
    ex = LLMServiceError()
    assert ex.detail == "Erro ao processar a resposta com o serviço LLM."
    assert ex.status_code == 503

def test_data_analysis_error_default():
    ex = DataAnalysisError()
    assert ex.detail == "Erro ao analisar os dados."
    assert ex.status_code == 500
