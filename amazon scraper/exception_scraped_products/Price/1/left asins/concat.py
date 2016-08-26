import pandas as pd
import os

all_files = os.listdir(".")

df = pd.DataFrame(columns = ['SKU', 'Price'])
for f in all_files:
    if f.startswith('updated'):
        temp = pd.read_csv(f)
        temp.columns = ['SKU', 'Price']
        df = pd.concat([df, temp], axis = 0)

df.to_csv('priceUpdated.csv', index = False)
