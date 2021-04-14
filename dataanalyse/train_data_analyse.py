'''
分析的数据范围包括：
1 不包含张脏数据和包含藏数据的比例
2 图片分辨率比例
3 四类动物数量比列
4 bbox数量极其规模比例
5 bbox大小与图片大小比例



6  统计每个图片对应的bbox的数量
'''
import os
from xml.dom.minidom import parse
import xml.etree.ElementTree as et

xml_path = "D:/Data/2021比赛数据集/水下光学/train/train/box/"
xml_files = os.listdir(xml_path)
all_pics = len(xml_files)
good_pics = 0
dirty_pics = 0
pic_resolution = {}  # 分辨率记录  格式是"1920-1080:num"
animal_num = {"holothurian": 0, "echinus": 0, "scallop": 0, "starfish": 0, "waterweeds": 0}  # 四类动物数量
num_bbox = 0
bbox_resolution = {}  # 分辨率记录  格式是"长-宽:num"
pic_bbox_scala_ratio = []  # 图片和bbox面积比列
no_bbox_num = 0  # 无边框

normal_info = open('normal_info.txt', 'w')
bbox_resolution_info = open('bbox_resolution_info.txt', 'w')
pic_bbox_scala_ratio_info = open('pic_bbox_scala_ratio_info.txt', 'w')
no_bbox_file_info = open('no_bbox_file_info.txt','w')


for xml in xml_files:
    if 'c' in xml:
        good_pics = good_pics + 1
    else:
        dirty_pics = dirty_pics + 1
    dom = et.parse(os.path.join(xml_path, xml))
    filename = dom.getroot()[0].text

    data = dom.getroot()[1:]
    # 记录图片分辨率
    pic_width = data[-1][0].text
    pic_heigth = data[-1][1].text
    pic_res_str = pic_width + "-" + pic_heigth
    if pic_res_str not in pic_resolution:
        pic_resolution[pic_res_str] = 1
    else:
        pic_resolution[pic_res_str] = pic_resolution[pic_res_str] + 1

    if len(data) <= 1:  # 计算无bbox
        no_bbox_file_info.writelines(filename + "\n")
        no_bbox_file_info.flush()
        no_bbox_num = no_bbox_num + 1
        continue

    for single_object in data[:-1]:
        num_bbox = num_bbox + 1
        name = single_object[0].text
        animal_num[name] = animal_num[name] + 1
        xmin = single_object[1][0].text
        ymin = single_object[1][1].text
        xmax = single_object[1][2].text
        ymax = single_object[1][3].text

        bbox_res_str = str(int(xmax) - int(xmin)) + "-" + str(int(ymax) - int(ymin))
        if bbox_res_str not in bbox_resolution:
            bbox_resolution[bbox_res_str] = 1
        else:
            bbox_resolution[bbox_res_str] = bbox_resolution[bbox_res_str] + 1

        pic_bbox_scala_ratio.append(
            int(pic_width) * int(pic_heigth) / ((int(xmax) - int(xmin)) * (int(ymax) - int(ymin))))

# 计算完成



no_bbox_file_info.close()

normal_info.writelines(
    "所有图片:{}     好数据:{}     脏数据:{}     无边框图片:{}\n".format(all_pics, good_pics, dirty_pics, no_bbox_num))

print("所有图片", all_pics, "好数据", good_pics, "脏数据", dirty_pics, "无边框图片", no_bbox_num)

normal_info.writelines("图片分辨率:{}\n".format(pic_resolution))
print("图片分辨率", pic_resolution)

normal_info.writelines("动物数量:{}\n".format(animal_num))
print("动物数量", animal_num)

normal_info.writelines("bbox的数量:{}\n".format(num_bbox))
print("bbox的数量\n", num_bbox)
normal_info.flush()
normal_info.close()

#pic_bbox_scala_ratio = [float(val) for val in pic_bbox_scala_ratio]
pic_bbox_scala_ratio.sort()
for ratio in pic_bbox_scala_ratio:
    pic_bbox_scala_ratio_info.writelines(str(ratio)+"\n")
    pic_bbox_scala_ratio_info.flush()

pic_bbox_scala_ratio_info.close()

for index, value in bbox_resolution.items():
    bbox_resolution_info.writelines("{}  {}\n".format(index, value))
    bbox_resolution_info.flush()

bbox_resolution_info.close()
