import xml.etree.ElementTree as ET
import shutil
import os

# TODO
# used PATHLIB imports

img = '/home/kurian/Projects/Objectdetection_SSD/data/JPEGImages/'
img_split = '/home/kurian/Projects/Objectdetection_SSD/data/ImageSplits/'
test = []
for f_name in os.listdir(img_split):
    if f_name.endswith('_train.txt'):
        test.append(str(f_name))
    print(test)
train = '/home/kurian/Projects/Objectdetection_SSD/train'
for f in test:
    with open(img_split+f) as t:
        for line in t:
            shutil.copy2(str(img+line.rstrip()), train)

