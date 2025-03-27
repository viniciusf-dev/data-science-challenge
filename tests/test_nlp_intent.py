from app.services.nlp_intent import detect_intent

def test_detect_intent_exact_match():
    question = "3 subcategorias de eletrônicos que mais utilizaram cartão de crédito"
    intent = detect_intent(question)
    assert intent == "top3_electronics_by_credit"

def test_detect_intent_similarity():
    question = "Quais são as categorias vendidas em maior quantidade?"
    intent = detect_intent(question)
    
    assert intent == "top_categories_by_quantity"
