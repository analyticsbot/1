import pandas as pd
import os

df = pd.read_csv('deduped_bsr.csv')
df1 = pd.read_csv('BSR_dl.csv')
df2 = pd.DataFrame(columns = ['SKU'])

for i, row in df.iterrows():
    sku=row[0]
    if df1.query('SKU == "' + sku +'"').shape[0]==0:
        nrows = df2.shape[0]
        df2.loc[nrows+1]=[sku]
df2.to_csv('left_asins.csv', index = False)
    
