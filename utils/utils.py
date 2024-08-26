import pandas as pd
import os

def loadData():
    data_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'Groceries_dataset.csv')
    df = pd.read_csv(data_path)
    return df

df = loadData()
print(df.head())