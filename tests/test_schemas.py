from app.models.schemas import QuestionRequest, GeneratedQuestion, FinalResponse, AnswerResponse

def test_question_request():
    req = QuestionRequest(question="Qual é o seu nome?")
    assert req.question == "Qual é o seu nome?"

def test_generated_question():
    gen = GeneratedQuestion(question="Pergunta", answer="Resposta")
    assert gen.question == "Pergunta"
    assert gen.answer == "Resposta"

def test_final_response():
    generated = [GeneratedQuestion(question="Pergunta 1", answer="Resposta 1")]
    final = FinalResponse(question="Pergunta principal", answer="Resposta principal", generated_questions=generated)
    assert final.question == "Pergunta principal"
    assert final.answer == "Resposta principal"
    assert len(final.generated_questions) == 1

def test_answer_response():
    answer = AnswerResponse(answer="Resposta simples")
    assert answer.answer == "Resposta simples"
