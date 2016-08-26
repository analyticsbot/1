import pandas as pd
import os

all_files = os.listdir(".")

df = pd.DataFrame(columns = ['SKU', 'Average_Customer_Review', 'Num_of_reviews'])
for f in all_files:
    if f.startswith('updated'):
        temp = pd.read_csv(f)
        temp.columns = ['SKU', 'Average_Customer_Review', 'Num_of_reviews']
        df = pd.concat([df, temp], axis = 0)

df.to_csv('ReviewsUpdated1.csv', index = False)
