from fastapi import APIRouter, HTTPException
from concurrent.futures import ThreadPoolExecutor

from app.models.schemas import QuestionRequest, FinalResponse, GeneratedQuestion
from app.services.analysis import DataAnalyzer
from app.services import nlp_intent
from app.services.llm_client import LLMClient
from app.services.data_loader import dataframe

router = APIRouter()
analyzer = DataAnalyzer(dataframe)
llm = LLMClient()

@router.post("/ask", response_model=FinalResponse)
def ask_question(request: QuestionRequest):
    question_text = request.question

    
    intent = nlp_intent.detect_intent(question_text)
    if not intent:
        raise HTTPException(
            status_code=400, 
            detail="Desculpe, não entendi a pergunta ou ela foge do escopo."
        )

    
    try:
        analysis_func = getattr(analyzer, intent)
    except AttributeError:
        raise HTTPException(
            status_code=500, 
            detail="Função não implementada para a intenção detectada."
        )

    
    data_result = analysis_func()

    
    with ThreadPoolExecutor() as executor:
        future_main = executor.submit(llm.format_answer_with_llm, question_text, data_result)
        future_additional = executor.submit(llm.generate_additional_questions_with_llm, question_text)

        llm_main_answer = future_main.result()
        additional_qas = future_additional.result()

    
    def process_question(item):
        q = item["question"]
        i = nlp_intent.detect_intent(q)
        if not i:
            return GeneratedQuestion(
                question=q, 
                answer="Desculpe, não entendi a pergunta ou ela foge do escopo."
            )
        try:
            f = getattr(analyzer, i)
            r = f()
            a = llm.format_answer_with_llm(q, r)
            return GeneratedQuestion(question=q, answer=a)
        except:
            return GeneratedQuestion(
                question=q, 
                answer="Função não implementada para a intenção detectada."
            )

    with ThreadPoolExecutor() as executor:
        futures = [executor.submit(process_question, item) for item in additional_qas]
        generated_questions = [f.result() for f in futures]

    
    final_response = FinalResponse(
        question=question_text,
        answer=data_result,
        generated_questions=generated_questions
    )
    return final_response
