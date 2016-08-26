import pandas as pd

df = pd.read_csv('priceUpdated_.csv')

df1 = pd.DataFrame(columns = ['SKU', 'Price'])

for i, row in df.iterrows():
    sku = row.tolist()[0]
    price = str(row.tolist()[1]).split('Save')[0]

    nrows = df1.shape[0]
    df1.loc[nrows+1]= [sku, price]

df1.to_csv('priceUpdated_1.csv', index = False)
    
