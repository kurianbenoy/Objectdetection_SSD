import xml.etree.ElementTree as ET
import shutil
import os

# TODO
# used PATHLIB imports

img = '/home/kurian/Projects/Objectdetection_SSD/data/JPEGImages/'
img_split = '/home/kurian/Projects/Objectdetection_SSD/data/ImageSplits/'
annRoot = '/home/kurian/Projects/Objectdetection_SSD/data/XMLAnnotations'
test = []
# for f_name in os.listdir(img_split):
#     if f_name.endswith('_train.txt'):
#         test.append(str(f_name))
#     print(test)
# train = '/home/kurian/Projects/Objectdetection_SSD/train'
# for f in test:
#     with open(img_split+f) as t:
#         for line in t:
#             shutil.copy2(str(img+line.rstrip()), train)

def extract_annotations(image_id,annRoot):
    res=[]
    width,height=0,0
    for file in os.listdir(annRoot):
        if file.startswith(image_id.split('.')[0]) and file.endswith('.xml'):
            extract=file
    tree=ET.parse(str(annRoot+extract))
    root=tree.getroot()
    return root

def parse_voc_xml(self, node):
        voc_dict = {}
        children = list(node)
        if children:
            def_dic = collections.defaultdict(list)
            for dc in map(self.parse_voc_xml, children):
                for ind, v in dc.items():
                    def_dic[ind].append(v)
            voc_dict = {
                node.tag:
                    {ind: v[0] if len(v) == 1 else v
                     for ind, v in def_dic.items()}
            }
        if node.text:
            text = node.text.strip()
            if not children:
                voc_dict[node.tag] = text
        return voc_dict

if __name__ == "__main__":
    node = extract_annotations('applauding_001.jpg', '/home/kurian/Projects/Objectdetection_SSD/data/XMLAnnotations/')
    #print(a.tag)
    l = parse_voc_xml(node)
    print(l)

