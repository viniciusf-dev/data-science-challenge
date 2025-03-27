import os
import google.generativeai as genai
import json
import logging

logging.basicConfig(level=logging.DEBUG, format="%(asctime)s [%(levelname)s] %(message)s")

GEMINI_KEY = os.getenv("GEMINI_API_KEY")

MODEL_NAME = "gemini-1.5-flash"

if GEMINI_KEY:
    genai.configure(api_key=GEMINI_KEY)

def clean_text(text: str) -> str:
    return " ".join(text.replace('"', '').split())

class LLMClient:
    def __init__(self, model_name: str = MODEL_NAME):
        self._gemini_enabled = bool(GEMINI_KEY)
        if self._gemini_enabled:
            self._model = genai.GenerativeModel(model_name=model_name)
        else:
            self._model = None

    def format_answer_with_llm(self, question: str, data_result) -> str:
        if not self._gemini_enabled:
            return str(data_result)
        prompt = f"""
        Você é um assistente que possui um conjunto de dados já filtrado e agregado.
        Pergunta do usuário: {question}
        Dados relevantes (já filtrados): {data_result}

        Instruções:
        - Elabore uma resposta clara, objetiva e completa, utilizando especificamente os dados fornecidos.
        - Responda de forma natural, humanizada e amigável, evitando qualquer formatação de código ou JSON.
        - Não insira quebras de linha desnecessárias; retorne o texto em um único parágrafo.
        - Utilize cumprimentos variados ou, se preferir, não use cumprimentos, apenas seja disposto.
        - Não invente dados; se algo não estiver em "data_result", não faça suposições.
        """
        try:
            response = self._model.generate_content(prompt)
            content = response.text.strip()
            content = content.replace("```", "").strip()
            content = clean_text(content)
            return content
        except Exception as e:
            logging.exception("Erro ao gerar resposta principal com LLM:")
            return f"[Erro ao gerar resposta principal com LLM: {str(e)}]"

    def generate_additional_questions_with_llm(self, original_question: str, data_result) -> list:
        if not self._gemini_enabled:
            return []
        prompt = f"""
            Você é um assistente especializado em análise de dados de vendas.
A pergunta original do usuário foi: "{original_question}"
Aqui está o resultado (parcial/filtrado) da análise, que pode servir de inspiração para novas perguntas:
{data_result}

Instruções:
1. Considere que o resultado acima contém dados concretos e já processados.
2. Crie exatamente 3 perguntas adicionais que explorem ou detalhem aspectos relacionados a esses dados.
   - As perguntas devem ser relevantes e coerentes com as informações em "data_result".
   - Evite gerar perguntas que não possam ser respondidas por meio dessas análises. Se a análise necessária não existir, retorne um disclaimer informando que não há dados suficientes.
3. As respostas curtas para cada pergunta também devem utilizar os dados disponíveis no dataset, conforme a análise realizada pelas funções citadas.
4. Atente-se ao fato de que as colunas presentes no dataset são: [
    OrderID,
    Product,
    Category,
    SubCategory,
    Quantity,
    UnitPrice,
    TotalPrice,
    Cost,
    Profit,
    PaymentMethod,
    OrderDate
   ]
   Portanto, as perguntas e respostas devem estar relacionadas a essas colunas.

IMPORTANTE: Retorne estritamente em JSON no seguinte formato:
[
  {{
    "question": "Pergunta 1",
    "answer": "Resposta curta"
  }},
  {{
    "question": "Pergunta 2",
    "answer": "Resposta curta"
  }},
  {{
    "question": "Pergunta 3",
    "answer": "Resposta curta"
  }}
]
        """
        try:
            response = self._model.generate_content(prompt)
            content = response.text.strip()
            logging.debug("LLM raw response for additional questions:\n%s", content)
            content = content.replace("```json", "").replace("```", "").strip()
            parsed = json.loads(content)
            if isinstance(parsed, list):
                final_list = []
                for item in parsed:
                    if isinstance(item, dict) and "question" in item and "answer" in item:
                        item["question"] = clean_text(item["question"])
                        item["answer"] = clean_text(item["answer"])
                        final_list.append(item)
                return final_list
            else:
                logging.error("JSON retornado não é uma lista: %s", parsed)
                return []
        except json.JSONDecodeError as jde:
            logging.error("Falha ao decodificar JSON das perguntas adicionais: %s", str(jde))
            logging.error("Conteúdo retornado:\n%s", content)
            return []
        except Exception as e:
            logging.exception("Erro ao gerar perguntas adicionais com LLM:")
            return [{
                "question": "[Erro na geração de perguntas adicionais]",
                "answer": f"[Detalhes do erro: {str(e)}]"
            }]
