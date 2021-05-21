import os
import glob
import shutil

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
        count = 0
        original = os.path.join(os.getcwd(), filename)
        target = r'C:\Users\james\Documents\final year project\coco\finalAnotation\\' +filename
        for line in lines:
            count += 1
    if(count >=1):
                shutil.copyfile(original, target)   
        