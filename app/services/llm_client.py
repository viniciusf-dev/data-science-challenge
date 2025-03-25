import os
import google.generativeai as genai
import json
import logging

logging.basicConfig(level=logging.DEBUG, format="%(asctime)s [%(levelname)s] %(message)s")

GEMINI_KEY = os.getenv("GEMINI_API_KEY")
MODEL_NAME = "gemini-1.5-flash"

genai.configure(api_key=GEMINI_KEY)

class LLMClient:
    def __init__(self, model_name: str = MODEL_NAME):
        self._model = genai.GenerativeModel(model_name=model_name)

    def format_answer_with_llm(self, question: str, data_result) -> str:


        prompt = f"""
            Você é um assistente que possui um conjunto de dados já filtrado e agregado.
            Pergunta do usuário: {question}
            Dados relevantes (já filtrados): {data_result}

            Instruções:
            - Elabore uma resposta clara, objetiva e completa, utilizando especificamente esses dados fornecidos.
            - Não invente dados; se algo não estiver em 'data_result', não suponha valores.
            - Retorne apenas o texto da resposta, sem formatação adicional, sem JSON.
"""

        try:
            response = self._model.generate_content(prompt)
            content = response.text.strip()

            content = content.replace("```", "").strip()

            return content

        except Exception as e:
            logging.exception("Erro ao gerar resposta principal com LLM:")
            return f"[Erro ao gerar resposta principal com LLM: {str(e)}]"

    def generate_additional_questions_with_llm(self, original_question: str) -> list:

        prompt = f"""
            Você é um assistente que conhece um dataset completo (não filtrado) de vendas.
            A pergunta original do usuário foi: '{original_question}'.

            Crie 3 novas perguntas que façam sentido, aprofundando ou explorando aspectos relacionados. 
            Para cada uma dessas 3 novas perguntas, elabore uma resposta curta usando o dataset fornecido em 
            Caso as informações não estejam disponíveis no dataset enviado a você, apenas diga que não sabe a resposta.


            IMPORTANTE: Retorne estritamente em JSON, no formato:
            [
            {{
                "question": "...",
                "answer": "... (com disclaimer)"
            }},
            {{
                "question": "...",
                "answer": "... (com disclaimer)"
            }},
            {{
                "question": "...",
                "answer": "... (com disclaimer)"
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
