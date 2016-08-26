import pandas as pd
import os

all_files = os.listdir(".")
all_files = [f for f in all_files if f.endswith('.csv')]

count = 0

complete = 'complete'
if not os.path.exists(complete):
    os.makedirs(complete)

incomplete = 'incomplete'
if not os.path.exists(incomplete):
    os.makedirs(incomplete)

for filename in all_files:
    df = pd.read_csv(filename)
    df1 = pd.DataFrame(columns = list(df.columns))

    for i, row in df.iterrows():
        if row['Stars_and_numbers'] not in ['{}'] and \
           row['Average_Customer_Review'] not in ['NA'] \
           and row['Dimensions'] not in ['{}']\
           and row['Shipping_Weight_Ounces'] not in ['NA'] \
           and row['Amazon_Best_Seller_Rank'] not in ['NA', ''] and \
           row['Num_of_reviews'] not in ['NA']:
            print 1
            count+=1
            nrow = df1.shape[0]
            df1.loc[nrow+1] = row

    if df1.shape>16:
        df1 = df1[:16]
        df1.to_csv(complete + '/' + filename, index = False)
    else:
        d = df.sort(['Stars_and_numbers', 'Average_Customer_Review','Dimensions','Shipping_Weight_Ounces', 'Amazon_Best_Seller_Rank', 'Num_of_reviews'], ascending = False)
        nrows = df1.shape
        temp = d[:16-nrows]
        df1 = pd.concat([df1, temp], axis =1)
        df1.to_csv(incomplete + '/' + filename, index = False)
    
print count
