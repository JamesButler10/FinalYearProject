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
            category = line.split(" ")[0]
            if(category=="5"):
                category="4"
            elif(category=="7"):
                category="5"
            boxX = float(line.split(" ")[1])
            boxY = float(line.split(" ")[2])
            boxWidth = float(line.split(" ")[3])
            boxHeight = float(line.split(" ")[4])
            boxX = boxX + boxWidth/2
            boxY = boxY + boxHeight/2
            newfile.write(str(category)+" "+str(boxX)+" "+str(boxY)+" "+str(boxWidth)+" "+str(boxHeight)+"\n")
