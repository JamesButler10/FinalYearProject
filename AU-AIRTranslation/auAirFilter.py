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
    with open(os.path.join(os.getcwd(), filename), 'w') as newfile:
        count = 0
        original = os.path.join(os.getcwd(), filename)
        target = r'C:\Users\james\Documents\final year project\auAir\\' +filename
        for line in lines:
            category = line.split(" ")[0]
            if(category=="1"):
                category="2"
            elif(category=="2"):
                category="5"
            elif(category=="3"):
                category="5"
            elif(category=="4"):
                category="3"
            elif(category=="5"):
                category="1"
            elif(category=="6"):
                category="4"
            elif(category=="7"):
                category="6"
            boxX = float(line.split(" ")[1])
            boxY = float(line.split(" ")[2])
            boxWidth = float(line.split(" ")[3])
            boxHeight = float(line.split(" ")[4])
            newfile.write(str(category)+" "+str(boxX)+" "+str(boxY)+" "+str(boxWidth)+" "+str(boxHeight)+"\n")
            count += 1
    if(count >=4):
                shutil.copyfile(original, target)        