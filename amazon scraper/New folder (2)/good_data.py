import pandas as pd
import os

all_files = os.listdir(".")
all_files = [f for f in all_files if f.endswith('.csv')]
print len(all_files)

directory = 'good_files'

if not os.path.exists(directory):
    os.makedirs(directory)
    
for file_ in all_files:
    df = pd.read_csv(file_)
    if (df.query('Average_Customer_Review == "NA"').shape[0] == 0) or\
       (df.query('Stars_and_numbers == "{}"').shape[0] == 0) or \
       (df.query('Num_of_reviews == "NA"').shape[0] == 0):
        shutil.move(file_, directory + '/' + file_)
        
