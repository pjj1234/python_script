import os
import random
from os.path import join
import aug
import Helpers as hp

from util import *

# ###########Pipeline##############
"""
1 准备数据集和yolo格式标签, 如果自己的数据集是voc或coco格式的，先转换成yolo格式，增强后在转回来
2 run crop_image.py  裁剪出目标并保存图片
3 run paste.py   随机将裁剪出目标图片贴到需要增强的数据集上，并且保存增强后的图片集和label文件
"""

base_dir = './'

save_base_dir = join(base_dir, 'save_path')

check_dir(save_base_dir)
# print(save_base_dir)

# imgs_dir = [f.strip() for f in open(join(base_dir, 'sea.txt')).readlines()]
imgs_dir = [os.path.join('Images', f) for f in os.listdir('Images') if f.endswith('jpg')]
labels_dir = hp.replace_labels(imgs_dir)
# print(imgs_dir, '\n', labels_dir)

# small_imgs_dir = [f.strip() for f in open(join(base_dir, 'dpj_small.txt')).readlines()]
small_imgs_dir = [os.path.join('bbox', f) for f in os.listdir('bbox') if f.endswith('jpg')]
random.shuffle(small_imgs_dir)  # 目标图片打乱
# print(small_imgs_dir)

times = 1  # 随机选择增加多少个目标

for image_dir, label_dir in zip(imgs_dir, labels_dir):
    # print(image_dir, label_dir)
    pic = cv2.imread(image_dir)
    pic_height, pic_width, pic_channel = pic.shape
    if pic_width >= 1000:
        small_img = []
        for x in range(times):
            if small_imgs_dir == []:
                small_imgs_dir = [os.path.join('bbox', f) for f in os.listdir('bbox') if f.endswith('jpg')]
                random.shuffle(small_imgs_dir)
            small_img.append(small_imgs_dir.pop())
        # print("ok")
        # print(small_img)
        aug.copysmallobjects(image_dir, label_dir, save_base_dir, small_img, times)
        print("=============图片处理完成！===============")
    else:
        print("图片太小，不增强")

print("=============全部处理完成！===============")
