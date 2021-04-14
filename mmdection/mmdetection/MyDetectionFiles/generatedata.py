# 本文主要是生成voc2007格式的数据

# 主要是生成三个Main文件夹下面的内容
import os
import sys
import random
img_path = r"/home/lywh/lywh-file-dir/data/underwater/underwatervoc2007/VOC2007/JPEGImages/"

train_file = open(
    "/home/lywh/lywh-file-dir/data/underwater/underwatervoc2007/VOC2007/ImageSets/Main/train.txt", 'w')
val_file = open(
    "/home/lywh/lywh-file-dir/data/underwater/underwatervoc2007/VOC2007/ImageSets/Main/val.txt", 'w')
test_file = open(
    "/home/lywh/lywh-file-dir/data/underwater/underwatervoc2007/VOC2007/ImageSets/Main/test.txt", 'w')
train_val_file = open(
    "/home/lywh/lywh-file-dir/data/underwater/underwatervoc2007/VOC2007/ImageSets/Main/trainval.txt", 'w')

img_list = os.listdir(img_path)

img_list = [img[:-4] for img in img_list]

print(img_list[0])

train_val_list = [img for img in img_list if len(img) > 6]
test_list = [img for img in img_list if len(img) == 6]

random.shuffle(train_val_list)

train_list = train_val_list[:int(len(train_val_list)*0.8)]
val_list = train_val_list[int(len(train_val_list)*0.8):]



print(train_val_list[1])

for img in test_list:
    test_file.write(img+'\n')
    test_file.flush()
test_file.close()

for img in train_list:
    train_file.write(img+"\n")
    train_file.flush()
train_file.close()


for img in val_list:
    val_file.write(img+"\n")
    val_file.flush()
val_file.close()


for img in train_val_list:
    train_val_file.write(img+"\n")
    train_val_file.flush()
train_val_file.close()