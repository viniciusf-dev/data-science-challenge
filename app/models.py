from pydantic import BaseModel
from typing import Any, List, Dict, Union

class QuestionRequest(BaseModel):
    question: str

class GeneratedQuestion(BaseModel):
    question: str
    answer: str

class FinalResponse(BaseModel):
    question: str
    
    answer: Union[str, float, List[Any], Dict[str, Any]]
    generated_questions: List[GeneratedQuestion]

class AnswerResponse(BaseModel):
    answer: str
