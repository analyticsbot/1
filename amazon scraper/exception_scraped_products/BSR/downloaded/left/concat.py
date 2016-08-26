import pandas as pd
import os

all_files = os.listdir(".")

df = pd.DataFrame(columns = ['SKU', 'Sales Rank'])
for f in all_files:
    if f.startswith('BS'):
        temp = pd.read_csv(f)
        temp.columns = ['SKU', 'Sales Rank']
        df = pd.concat([df, temp], axis = 0)

df.to_csv('BSR_vf.csv', index = False)
