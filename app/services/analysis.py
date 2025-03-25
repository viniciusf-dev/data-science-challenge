import pandas as pd
from typing import List, Dict, Any

class DataAnalyzer:
    def __init__(self, df: pd.DataFrame):
        self._df = df.copy()

    def top3_electronics_by_credit(self) -> List[Dict[str, Any]]:
        mask = (self._df['Category'] == 'Eletrônicos') & (self._df['PaymentMethod'] == 'Cartão de Crédito')
        subset = self._df[mask]
        top_subcats = subset['SubCategory'].value_counts().nlargest(3)
        return [{"subcategory": sub, "count": int(count)} for sub, count in top_subcats.items()]

    def top_categories_by_quantity(self) -> List[Dict[str, Any]]:
        category_sums = self._df.groupby('Category')['Quantity'].sum().sort_values(ascending=False)
        return [{"category": cat, "quantity": int(qty)} for cat, qty in category_sums.items()]

    def subcategories_highest_avg_value(self) -> List[Dict[str, Any]]:
        avg_values = self._df.groupby('SubCategory').apply(lambda g: g['TotalPrice'].sum() / g['Quantity'].sum())
        top_subcats = avg_values.sort_values(ascending=False).head(5)
        return [{"subcategory": sub, "avg_item_value": round(val, 2)} for sub, val in top_subcats.items()]

    def top2_payment_methods(self) -> List[Dict[str, Any]]:
        top_methods = self._df['PaymentMethod'].value_counts().nlargest(2)
        return [{"payment_method": method, "count": int(count)} for method, count in top_methods.items()]

    def avg_profit_by_category(self) -> Dict[str, float]:
        avg_profit = self._df.groupby('Category')['Profit'].mean().round(2)
        return {cat: float(profit) for cat, profit in avg_profit.items()}

    def worst3_products_by_loss(self) -> List[Dict[str, Any]]:
        losses = self._df[self._df['Profit'] < 0][['Product', 'Profit']]
        worst3 = losses.nsmallest(3, 'Profit')
        return [{"product": prod, "loss": float(profit)} for prod, profit in zip(worst3['Product'], worst3['Profit'])]

    def avg_ticket_by_category(self) -> Dict[str, float]:
        total_revenue = self._df.groupby('Category')['TotalPrice'].sum()
        total_orders = self._df.groupby('Category')['OrderID'].nunique()
        avg_ticket = (total_revenue / total_orders).round(2)
        return {cat: float(val) for cat, val in avg_ticket.items()}

    def least_selling_subcategory(self) -> Dict[str, Any]:
        grouped = self._df.groupby('SubCategory')['Quantity'].sum()
        min_val = grouped.min()
        subcats = grouped[grouped == min_val].index.tolist()
        return {"subcategory": subcats[0], "quantity": int(min_val)}

    def avg_profit_per_order(self) -> float:
        total_profit = self._df['Profit'].sum()
        total_orders = self._df['OrderID'].nunique()
        if total_orders == 0:
            return 0.0
        return round(float(total_profit / total_orders), 2)
