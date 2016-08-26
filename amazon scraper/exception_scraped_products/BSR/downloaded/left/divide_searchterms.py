import csv
import os
f = open('left_asins.csv', 'rb')
data = f.read().split('\n')[:-1]
data = [d.strip() for d in data]

count =1
if not os.path.exists(str(count)):
    os.makedirs(str(count))
f = open(str(count) + '/'+ 'LEFT_ASIN_BSR_'+str(count)+'.csv', 'wb')
writer = csv.writer(f)

file_=2
for line in data:
    line = line.strip()
    writer.writerow([line])
    count+=1
    if count % 1000==0:
        f.close()
        if not os.path.exists(str(file_)):
            os.makedirs(str(file_))
        f = open(str(file_) + '/' +'LEFT_ASIN_BSR_'+str(file_)+'.csv', 'wb')
        writer = csv.writer(f)
        file_+=1
    line_split = line.split()
    if len(line_split) == 0:
        break

f.close()
        
    
    
