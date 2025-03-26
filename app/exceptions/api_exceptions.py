class APIException(Exception):

    def __init__(self, detail: str, status_code: int = 500):
        self.detail = detail
        self.status_code = status_code
        super().__init__(detail)

class IntentNotRecognized(APIException):
    def __init__(self, detail: str = "Desculpe, não entendi a pergunta ou ela foge do escopo."):
        super().__init__(detail, status_code=400)

class FunctionNotImplemented(APIException):
    def __init__(self, detail: str = "Função não implementada para a intenção detectada."):
        super().__init__(detail, status_code=501)

class LLMServiceError(APIException):
    def __init__(self, detail: str = "Erro ao processar a resposta com o serviço LLM.", status_code: int = 503):
        super().__init__(detail, status_code=status_code)

class DataAnalysisError(APIException):
    def __init__(self, detail: str = "Erro ao analisar os dados.", status_code: int = 500):
        super().__init__(detail, status_code=status_code)
