import pandas as pd
import os

def load_dataset(path="data/product_order_details.csv") -> pd.DataFrame:

    if not os.path.isabs(path):

        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        path = os.path.join(base_dir, path)
    
    
    df = pd.read_csv(path)

    df.columns = df.columns.str.strip()

    numeric_cols = ['OrderID', 'Quantity', 'UnitPrice', 'TotalPrice', 'Cost', 'Profit']
    for col in numeric_cols:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors='coerce')

    return df


dataframe = load_dataset()
