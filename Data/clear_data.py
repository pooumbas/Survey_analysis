import os

all_files=os.listdir()

for file in all_files:
    filename, file_extension = os.path.splitext(file)
    if file_extension=='.json' or file_extension=='.png' or file_extension=='.txt':
        os.remove(file)
        print(file+" removed.....")

