import pandas as pd
import pytest
from app.services.analysis import DataAnalyzer

@pytest.fixture
def sample_df():
    data = {
        "Category": ["Eletrônicos", "Eletrônicos", "Eletrodomésticos", "Eletrônicos"],
        "PaymentMethod": ["Cartão de Crédito", "Cartão de Crédito", "Dinheiro", "Cartão de Crédito"],
        "SubCategory": ["A", "B", "C", "A"],
        "Quantity": [10, 5, 20, 15],
        "TotalPrice": [100, 50, 200, 150],
        "Profit": [20, 5, -10, 15],
        "OrderID": [1, 2, 3, 4]
    }
    return pd.DataFrame(data)

def test_top3_electronics_by_credit(sample_df):
    analyzer = DataAnalyzer(sample_df)
    result = analyzer.top3_electronics_by_credit()

    assert {"subcategory": "A", "count": 2} in result
    assert {"subcategory": "B", "count": 1} in result

def test_top_categories_by_quantity(sample_df):
    analyzer = DataAnalyzer(sample_df)
    result = analyzer.top_categories_by_quantity()
    
    assert {"category": "Eletrônicos", "quantity": 30} in result
    assert {"category": "Eletrodomésticos", "quantity": 20} in result
