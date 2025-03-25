import spacy

nlp = spacy.load("pt_core_news_sm")

intent_phrases = {
    "top3_electronics_by_credit": [
        "3 subcategorias de eletrônicos que mais utilizaram cartão de crédito"
    ],
    "top_categories_by_quantity": [
        "categorias vendidas em maior quantidade"
    ],
    "subcategories_highest_avg_value": [
        "subcategorias com maior valor médio por item"
    ],
    "top2_payment_methods": [
        "2 métodos de pagamento mais utilizados"
    ],
    "avg_profit_by_category": [
        "lucro médio por categoria de produto"
    ],
    "worst3_products_by_loss": [
        "3 produtos com maior prejuízo"
    ],
    "avg_ticket_by_category": [
        "ticket médio por categoria"
    ],
    "least_selling_subcategory": [
        "subcategoria com menor quantidade de vendas"
    ],
    "avg_profit_per_order": [
        "média de lucro por transação"
    ]
}

def detect_intent(question: str) -> str:
    try:
        doc = nlp(question)
    except Exception:
        return ""
    for intent, phrases in intent_phrases.items():
        for phrase in phrases:
            if phrase.lower() in question.lower():
                return intent
    best_intent = ""
    best_score = 0.0
    for intent, ref_phrases in intent_phrases.items():
        for ref_text in ref_phrases:
            try:
                ref_doc = nlp(ref_text)
                score = doc.similarity(ref_doc)
                if score > best_score:
                    best_score = score
                    best_intent = intent
            except Exception:
                continue
    return best_intent
