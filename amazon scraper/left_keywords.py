import pandas as pd
import os

def cleanKeyword(row):
    return row[0].strip().replace('"','').replace("'",'').replace("/",' ')

df = pd.read_csv('Keywords_Full.csv')

df = df.apply(cleanKeyword, axis=1)

all_files = os.listdir(".")
all_files = [f for f in all_files if f.endswith('.csv')]
print len(all_files)

df1 = pd.DataFrame(columns = ['not downloaded'])

for fil in all_files:
    fil = fil[:-4]
    if df.query('Keywords == "'+ fil + '"').shape[0]==0:
        shape = df1.shape[0]
        df1.iloc[shape+1] = [fil]

df1.to_csv('not_downloaded_keywords.csv', index = False, encoding = 'utf-8')
        
