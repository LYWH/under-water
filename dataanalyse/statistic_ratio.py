
ratio = []

with open('pic_bbox_scala_ratio_info.txt', 'r') as f:
   ratio = f.readlines()

ratio = [float(temp) for temp in ratio]

