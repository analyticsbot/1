import csv

f = open('Keywords_Full.csv', 'rb')
data = f.read().split('\n')[:-1]
data = [d.strip() for d in data]

count =1
f = open('Keywords_'+str(count)+'.csv', 'wb')
writer = csv.writer(f)

file_=2
for line in data:
    line = line.strip()
    writer.writerow([line])
    count+=1
    if count % 41900==0:
        f.close()
        f = open('Keywords_'+str(file_)+'.csv', 'wb')
        writer = csv.writer(f)
        file_+=1
    line_split = line.split()
    if len(line_split) == 0:
        break

f.close()
        
    
    
