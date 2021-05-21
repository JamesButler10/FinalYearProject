import os
import glob

CATEGORIES = {
    0: "person",
    1: "bicycle",
    2: "car",
    3: "motorcycle",
    5: "bus",
    7: "truck"
}

current = 0

for filename in glob.glob('*.txt'):
    print(f'current file : {current}')
    current += 1
    with open(os.path.join(os.getcwd(), filename), 'r') as f:
        lines = f.readlines()
    with open(os.path.join(os.getcwd(), filename), 'w') as newfile:
        for line in lines:
            category = int(line.split(" ")[0])
            if category in CATEGORIES.keys():
                print(line, end="", file=newfile)
