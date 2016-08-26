import os

all_files = os.listdir(".")
all_files = [f for f in all_files if f.endswith('csv__')]
print len(all_files)

for file_ in all_files:
    try:
        os.remove(file_[:-2])
    except:
        pass
    os.rename(file_, file_[:-2])
