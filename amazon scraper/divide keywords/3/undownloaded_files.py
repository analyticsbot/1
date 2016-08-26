import os
import pandas as pd

df = pd.DataFrame(columns = ['File'])

main_dir_files = os.listdir(main_dir)
dl_dir_files = os.listdir(dl_dir)

for f in dl_dir_files:
    if f not in main_dir_files:
        n = df.shape[0]
        df.loc[n+1] = [f]
df.to_csv('notDownloaded.csv')
