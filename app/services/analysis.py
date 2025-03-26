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

   

    def items_sold_by_subcategory(self) -> List[Dict[str, Any]]:
        
        totals = self._df.groupby('SubCategory')['Quantity'].sum()
        return [{"subcategory": sub, "total_sold": int(qty)} for sub, qty in totals.items()]

    def variation_percentage_avg_value(self) -> Dict[str, Any]:

        avg_values = self._df.groupby('SubCategory').apply(lambda g: g['TotalPrice'].sum() / g['Quantity'].sum())
        if avg_values.empty:
            return {"error": "Dados insuficientes para calcular a variação."}
        max_sub = avg_values.idxmax()
        min_sub = avg_values.idxmin()
        max_val = avg_values.max()
        min_val = avg_values.min()
        if min_val == 0:
            return {"error": "Valor mínimo é zero, não é possível calcular variação percentual."}
        variation = round(((max_val - min_val) / min_val) * 100, 2)
        return {
            "max_subcategory": max_sub,
            "max_value": round(max_val, 2),
            "min_subcategory": min_sub,
            "min_value": round(min_val, 2),
            "variation_percentage": variation
        }

    def sum_avg_values_for_subcategories(self, subcategories: List[str] = None) -> Dict[str, Any]:

        avg_values = self._df.groupby('SubCategory').apply(lambda g: g['TotalPrice'].sum() / g['Quantity'].sum())
        result = {}
        if subcategories is None:
            subcategories = list(avg_values.index)
        for sub in subcategories:
            if sub in avg_values.index:
                result[sub] = round(avg_values.loc[sub], 2)
            else:
                result[sub] = None
        if all(value is not None for value in result.values()):
            total_sum = sum(result.values())
            return {"subcategories": result, "total_sum": round(total_sum, 2)}
        else:
            missing = [sub for sub, value in result.items() if value is None]
            return {"subcategories": result, "total_sum": None, "error": f"Subcategorias não encontradas: {', '.join(missing)}"}

    def total_sales_by_category(self, categories: List[str] = None) -> Dict[str, Any]:

        df = self._df
        if categories:
            df = df[df['Category'].isin(categories)]
        sales = df.groupby('Category')['TotalPrice'].sum().round(2)
        return {cat: float(val) for cat, val in sales.items()}

    def sales_proportion_electronics_vs_home_appliances(self) -> Dict[str, Any]:

        df = self._df[self._df['Category'].isin(['Eletrônicos', 'Eletrodomésticos'])]
        sales = df.groupby('Category')['TotalPrice'].sum()
        total = sales.sum()
        if total == 0:
            return {"error": "Total de vendas zero, não é possível calcular proporção."}
        proportion = {cat: round((val/total)*100, 2) for cat, val in sales.items()}
        return proportion

    def best_selling_product_by_category(self) -> Dict[str, Any]:

        df = self._df[self._df['Category'].isin(['Eletrônicos', 'Eletrodomésticos'])]
        grouped = df.groupby(['Category', 'Product'])['Quantity'].sum()
        result = {}
        for category in ['Eletrônicos', 'Eletrodomésticos']:
            cat_group = grouped[category]
            if not cat_group.empty:
                best_product = cat_group.idxmax()
                result[category] = {"product": best_product, "quantity": int(cat_group.max())}
            else:
                result[category] = {"error": "Sem dados para esta categoria"}
        return result

    def profit_margin_by_category(self) -> Dict[str, Any]:

        df = self._df[self._df['Category'].isin(['Eletrônicos', 'Eletrodomésticos'])]
        grouped = df.groupby('Category').agg({'Profit': 'sum', 'TotalPrice': 'sum'})
        result = {}
        for cat in grouped.index:
            total_price = grouped.loc[cat, 'TotalPrice']
            if total_price == 0:
                result[cat] = {"error": "TotalPrice é zero, não é possível calcular margem."}
            else:
                margin = round((grouped.loc[cat, 'Profit'] / total_price) * 100, 2)
                result[cat] = margin
        return result

    def percentage_sales_by_category(self) -> Dict[str, Any]:

        return self.sales_proportion_electronics_vs_home_appliances()

    def credit_card_sales_proportion(self) -> Dict[str, Any]:

        total_sales = self._df['TotalPrice'].sum()
        cc_sales = self._df[self._df['PaymentMethod'] == 'Cartão de Crédito']['TotalPrice'].sum()
        if total_sales == 0:
            return {"error": "Total de vendas zero, não é possível calcular proporção."}
        proportion = round((cc_sales / total_sales) * 100, 2)
        return {"credit_card_sales_percentage": proportion}

    def avg_item_value_variation_peripherals_over_time(self) -> Any:

        if 'OrderDate' not in self._df.columns:
            return {"error": "Coluna 'OrderDate' não encontrada no conjunto de dados."}
        df_peripherals = self._df[self._df['SubCategory'] == 'Periféricos'].copy()
        try:
            df_peripherals['OrderDate'] = pd.to_datetime(df_peripherals['OrderDate'])
        except Exception as e:
            return {"error": f"Erro ao converter 'OrderDate': {str(e)}"}
        
        df_peripherals['YearMonth'] = df_peripherals['OrderDate'].dt.to_period('M')
        grouped = df_peripherals.groupby('YearMonth').apply(lambda g: g['TotalPrice'].sum() / g['Quantity'].sum())
        result = [{"year_month": str(period), "avg_item_value": round(val, 2)} for period, val in grouped.items()]
        return result

    def most_profitable_product_by_category(self) -> Dict[str, Any]:

        grouped = self._df.groupby(['Category', 'Product'])['Profit'].sum()
        result = {}
        for category in self._df['Category'].unique():
            cat_group = grouped[category]
            if not cat_group.empty:
                best_product = cat_group.idxmax()
                result[category] = {"product": best_product, "total_profit": round(float(cat_group.max()), 2)}
            else:
                result[category] = {"error": "Sem dados para esta categoria"}
        return result
