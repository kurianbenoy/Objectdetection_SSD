import xml.etree.ElementTree as ET
import shutil
import os

# TODO
# used PATHLIB imports

img = '/home/kurian/Projects/Objectdetection_SSD/data/JPEGImages/'
img_split = '/home/kurian/Projects/Objectdetection_SSD/data/ImageSplits/'
annRoot = '/home/kurian/Projects/Objectdetection_SSD/data/XMLAnnotations'
test = []


def extract_annotations(image_id,annRoot):
    res=[]
    width,height=0,0
    for file in os.listdir(annRoot):
        if file.startswith(image_id.split('.')[0]) and file.endswith('.xml'):
            extract=file
    tree=ET.parse(str(annRoot+extract))
    root=tree.getroot()
    return root

# def parse_voc_xml(self, node):
#         voc_dict = {}
#         children = list(node)
#         if children:
#             def_dic = collections.defaultdict(list)
#             for dc in map(self.parse_voc_xml, children):
#                 for ind, v in dc.items():
#                     def_dic[ind].append(v)
#             voc_dict = {
#                 node.tag:
#                     {ind: v[0] if len(v) == 1 else v
#                      for ind, v in def_dic.items()}
#             }
#         if node.text:
#             text = node.text.strip()
#             if not children:
#                 voc_dict[node.tag] = text
#         return voc_dict


for obj in target.iter('object'):
            name = obj.find('action').text.lower().strip()
            bbox = obj.find('bndbox')

            pts = ['xmin', 'ymin', 'xmax', 'ymax']
            bndbox = []
            for i, pt in enumerate(pts):
                cur_pt = int(bbox.find(pt).text) - 1
                # scale height or width
                cur_pt = cur_pt / width if i % 2 == 0 else cur_pt / height
                bndbox.append(cur_pt)
            label_idx = self.class_to_ind[name]
            bndbox.append(label_idx)
            res += [bndbox]  # [xmin, ymin, xmax, ymax, label_ind]
            # img_id = target.find('filename').text[:-4]

        return res

if __name__ == "__main__":
    node = extract_annotations('applauding_001.jpg', '/home/kurian/Projects/Objectdetection_SSD/data/XMLAnnotations/')
    #print(a.tag)
    l = parse_voc_xml(node)
    print(l)

