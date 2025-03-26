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
    ],
    
    "total_sales_electronics_home_appliances": [
        "valor total de vendas para cada categoria (Eletrônicos e Eletrodomésticos) considerando a quantidade vendida",
        "total de vendas por categoria (Eletrônicos e Eletrodomésticos) considerando a quantidade vendida"
    ],
    "sales_proportion_electronics_vs_home_appliances": [
        "proporção de vendas entre a categoria 'Eletrônicos' e 'Eletrodomésticos'",
        "relação de vendas entre Eletrônicos e Eletrodomésticos"
    ],
    "best_selling_product_by_category": [
        "produto mais vendido dentro de cada categoria entre Eletrônicos e Eletrodomésticos",
        "qual o produto mais vendido em Eletrônicos e Eletrodomésticos"
    ],
    "profit_margin_by_category": [
        "margem de lucro percentual para cada categoria (Eletrodomésticos e Eletrônicos)",
        "percentual de lucro por categoria para Eletrônicos e Eletrodomésticos"
    ],
    "total_sales_by_category": [
        "valor total de vendas para cada categoria (Eletrônicos e Eletrodomésticos)",
        "total de vendas para Eletrônicos e Eletrodomésticos"
    ],
    "percentage_sales_by_category": [
        "proporção percentual de vendas de Eletrônicos e Eletrodomésticos em relação ao total",
        "percentual de vendas por categoria entre Eletrônicos e Eletrodomésticos"
    ],
    "credit_card_sales_proportion": [
        "proporção de vendas realizadas via Cartão de Crédito em relação ao total de vendas",
        "percentual de vendas com cartão de crédito"
    ],
    "avg_item_value_variation_peripherals_over_time": [
        "variação do valor médio por item na subcategoria 'Periféricos' ao longo do tempo",
        "evolução do valor médio por item em Periféricos ao longo do tempo"
    ],
    "most_profitable_product_by_category": [
        "produto mais lucrativo por categoria",
        "qual o produto mais lucrativo em cada categoria"
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
