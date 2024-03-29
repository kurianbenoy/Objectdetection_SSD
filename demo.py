import os
import sys
import torch
import torch.nn as nn
import torch.backends.cudnn as cudnn
from torch.autograd import Variable
import numpy as np
import cv2
from ssd import build_ssd
from matplotlib import pyplot as plt
from data import VOCDetection, VOC_ROOT, VOCAnnotationTransform
import random
from data import VOC_CLASSES as labels

model='vgg'
samples=10
display=True

if torch.cuda.is_available():
    torch.set_default_tensor_type('torch.cuda.FloatTensor')
    
dir_path = os.path.dirname(os.path.realpath(__file__))
#cwd = os.getcwd()

'''
Build SSD300 in Test Phase
'''

net = build_ssd('test',300, 21)    # initialize SSD
net.load_weights('weights/ssd_300_VOC0712.pth')
'''
Load Image
'''
testset = VOCDetection(VOC_ROOT, [('2007', 'test')], None, VOCAnnotationTransform())
ids=len(testset.ids)

img_ids = random.sample(range(ids),samples)
for img_id in img_ids:
    image = testset.pull_image(img_id)
    rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    # View the sampled input image before transform
    if display:
        plt.figure(figsize=(10,10))
        plt.imshow(rgb_image)
        plt.show()
    
    '''
    Pre-process the input.
    For SSD, at test time we use a custom BaseTransform callable to resize our image 
    to 300x300, subtract the dataset's mean rgb values, and swap the color channels 
    for input to SSD300.
    '''
    x = cv2.resize(image, (300, 300)).astype(np.float32)
    x -= (104.0, 117.0, 123.0)
    x = x.astype(np.float32)
    x = x[:, :, ::-1].copy()
    #plt.imshow(x)
    x = torch.from_numpy(x).permute(2, 0, 1)
    xx = Variable(x.unsqueeze(0))     # wrap tensor in Variable
    if torch.cuda.is_available():
        xx = xx.cuda()
    y = net(xx)
    
    '''
    Parse the Detections and View Results
    Filter outputs with confidence scores lower than a threshold Here we choose 60%
    '''
    
    
    top_k=10
    
    plt.figure(figsize=(10,10))
    colors = plt.cm.hsv(np.linspace(0, 1, 21)).tolist()
    
    plt.imshow(rgb_image)  # plot the image for matplotlib
    currentAxis = plt.gca()
    detections = y.data
    # scale each detection back up to the image
    scale = torch.Tensor(rgb_image.shape[1::-1]).repeat(2)
    for i in range(detections.size(1)):
        j = 0
        while detections[0,i,j,0] >= 0.6:
            score = detections[0,i,j,0]
            label_name = labels[i-1]
            display_txt = '%s: %.2f'%(label_name, score)
            pt = (detections[0,i,j,1:]*scale).cpu().numpy()
            coords = (pt[0], pt[1]), pt[2]-pt[0]+1, pt[3]-pt[1]+1
            color = colors[i]
            currentAxis.add_patch(plt.Rectangle(*coords, fill=False, edgecolor=color, linewidth=2))
            currentAxis.text(pt[0], pt[1], display_txt, bbox={'facecolor':color, 'alpha':0.5})
            j+=1
    plt.savefig(os.path.join(dir_path,'demo','output'+str(img_id)+'.png'))



