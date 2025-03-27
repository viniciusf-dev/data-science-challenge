# Data Science Challenge - Logcomex

Este repositório contém uma solução para o desafio técnico da Logcomex. O projeto consiste em uma API REST em Python que processa perguntas em linguagem natural, filtrando e analisando os dados do dataset de pedidos de produtos para retornar respostas precisas. Além disso, a solução utiliza boas práticas de desenvolvimento, testes automatizados e documentação interativa via Swagger.

---

## 📌 Funcionalidades

- **Processamento de Perguntas:** Interpretação de linguagem natural para identificar a intenção do usuário e direcionar a consulta ao dataset.
- **Consultas Específicas:** Funções dedicadas para responder perguntas específicas (ex.: subcategorias de eletrônicos, categorias mais vendidas, lucro médio, etc.).
- **Geração de Insights:** Criação de perguntas adicionais com LLM utilizando como base o dataset e a pergunta original para extrair novos insights.
- **Documentação Interativa:** API documentada automaticamente com Swagger, acessível via `/docs`.
- **Testes Automatizados:** Conjunto de testes para garantir a qualidade e robustez do código.
- **Integração com Gemini API:** Humanização das respostas e geração de perguntas complementares utilizando a API Gemini (configuração via variável de ambiente).

---

## 📂 Estrutura do Projeto

```bash
data-science-challenge/
├── app/
│   ├── data/
│   │   └── product_order_details.csv
│   ├── exceptions/
│   │   └── api_exceptions.py
│   ├── middlewares/
│   │   └── error_handler.py
│   ├── models/
│   │   └── schemas.py
│   ├── routers/
│   │   └── questions.py
│   └── services/
│       ├── analysis.py
│       ├── data_loader.py
│       ├── llm_client.py
│       ├── nlp_intent.py
│       ├── __init__.py
│       └── main.py
└── tests/
    ├── test_api_exception.py
    ├── test_data_analyzer.py
    ├── test_llm_client.py
    ├── test_middlewares.py
    ├── test_nlp_intent.py
    ├── test_router_questions.py
    └── test_schemas.py

```

---

## 🚀 Como Rodar Localmente

1. **Clone o repositório:**

   ```bash
   git clone https://github.com/viniciusf-dev/data-science-challenge.git
   cd data-science-challenge
   ```

2. **Crie e ative um ambiente virtual:**

   ```bash
   python3 -m venv venv
   source venv/bin/activate  # Linux/Mac
   # ou, no Windows:
   venv\Scripts\activate
   ```

3. **Instale as dependências:**

   ```bash
   pip install -r requirements.txt
   ```

5. **Instale o modelo utilizado do Spacy:**

   ```bash
   python -m spacy download pt_core_news_sm
   ```

6. **Configuração da Chave de API da Gemini:**

   - Renomeie o arquivo `.env.example` para `.env` e insira sua chave de API na variável `GEMINI_API_KEY`.
   - Para obter sua chave gratuita do Gemini, basta acessar [GET API key | Google AI Studio](https://aistudio.google.com/apikey) e então criá-la.
   - É muito <b>importante</b> configurar a chave da API do Gemini, para obter respostas humanizadas e perguntas adicionais geradas pelo LLM.

7. **Execute a API:**

   ```bash
   uvicorn app.main:app
   ```

   A API estará disponível em: [http://127.0.0.1:8000](http://127.0.0.1:8000)

---

## 🤖 Interagindo com o Modelo 

Após iniciar a API, envie uma requisição com o método POST passando a chave `question` no body da requisição para a rota [http://127.0.0.1:8000/ask](http://127.0.0.1:8000/ask)

   ```bash
  {"question": "Quais as categorias vendidas em maior quantidade?"}
   ```

---

## 📝 Documentação da API

Após iniciar a API, acesse a documentação interativa (Swagger) em:

[http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

---

## 🔍 Testes

Os testes foram desenvolvidos utilizando **pytest**. Para executar os testes, vá até a raiz do projeto e execute:

```bash
python -m pytest
```
---

## 🖼️ Demonstração

![image](https://github.com/user-attachments/assets/b16191eb-979b-41a5-985e-45c1f9e0fac7)


### Exemplo de Demonstração

![image](https://github.com/user-attachments/assets/02e5530e-050d-4038-92fc-bf794a6e3ad6)
---

## 🔧 Possíveis Melhorias

- **NLP Avançado:** Atualizar o algoritmo atual para uma LLM capaz de gerar queries dinâmicas e interpretar os resultados para respostas mais precisas.
- **Otimização de Performance:** Revisar e otimizar funções de manipulação de dados para maior eficiência.

---

## 🛠️ Tecnologias e Bibliotecas Utilizadas

| Tecnologia/Lib     | Versão/Relevância   | Descrição                                                      |
|--------------------|---------------------|------------------------------------------------------------------|
| **Python**         | 3.12                | Linguagem principal do projeto.                                  |
| **FastAPI**        | 0.115.12            | Framework utilizado para criação da API REST.                    |
| **Pandas**         | 2.2.3               | Biblioteca para manipulação e análise dos dados.                 |
| **Pydantic**       | 2.10.6              | Validação de inputs e definição de schemas.                      |
| **Swagger**        | Integrado com FastAPI | Documentação interativa da API (acessível em `/docs`).             |
| **spaCy**          | 3.8.4               | Utilizado para NLP e detecção de intenções (pode ser ajustado).    |
| **Gemini API**     | 0.8.4               | Integração para humanização das respostas via API externa.         |
| **pytest**         | 8.3.5               | Framework para execução dos testes automatizados.                |
