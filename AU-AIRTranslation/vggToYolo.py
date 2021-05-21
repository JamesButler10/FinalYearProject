import sys
import json
from PIL import Image
from decimal import Decimal

counts = {}


def get_object_class(region, filename, names):
    if region['region_attributes'] == {}:
        return None

    category = region['region_attributes']['Categories']

    name = category
    index = [item.lower() for item in names].index(name.lower())

    if category in counts:
        counts[category] += 1
    else:
        counts[category] = 1

    return index


def get_dark_annotation(region, size):
    x = region['shape_attributes']['x']
    y = region['shape_attributes']['y']
    width = region['shape_attributes']['width']
    height = region['shape_attributes']['height']

    # relative position of center x of rect
    _x = Decimal(x + width/2) / Decimal(size[0])
    # relative position of center y of rect
    _y = Decimal(y + height/2) / Decimal(size[1])
    _width = Decimal(width / size[0])
    _height = Decimal(height / size[1])

    return f'{_x:.10f} {_y:.10f} {_width:.10f} {_height:.10f}'


def main():
    splitter = 0
    with open(sys.argv[1:][0]) as file:
        annotations = json.load(file)['_via_img_metadata']

        try:
            namesFile = sys.argv[1:][1]
            names = open(namesFile).read().split('\n')
        except IndexError:
            print >> sys.stderr, "names file's missing from argument.\n\tnamesFile = sys.argv[1:][1]\nIndexError: list index out of range"

        for key in dict(annotations).keys():
            image = annotations[key]

            imageName = image['filename']
            filename = imageName.split('.', 1)[0]

            regions = image['regions']

            try:
                img = Image.open(imageName)
            except IOError:
                print(sys.stderr + "No such file" + imageName)

            content = ""
            for region in regions:
                obj_class = get_object_class(region, imageName, names)
                if obj_class == None:
                    continue
                annotation = get_dark_annotation(region, img.size)
                content += f'{obj_class} {annotation}\n'

            with open(f'./{filename}.txt', "w") as outFile:
                outFile.write(content)

            if splitter < 7:
                with open(f'../train.txt', "a") as outFile:
                    outFile.write(f'data/obj/{imageName}\n')
                splitter += 1
            elif splitter < 9:
                with open(f'../valid.txt', "a") as outFile:
                    outFile.write(f'data/obj/{imageName}\n')
                splitter += 1
            else:
                with open(f'../test.txt', "a") as outFile:
                    outFile.write(f'data/obj/{imageName}\n')
                splitter = 0

        with open(f'./counts.json', "w") as outFile:
            outFile.write(json.dumps(counts))


if __name__ == "__main__":
    main()
