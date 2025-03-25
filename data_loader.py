# data_loader.py
import pandas as pd

def load_dataset(path: str) -> pd.DataFrame:
    df = pd.read_csv(path)

    return df

dataframe = load_dataset("data/product_order_details.csv")
