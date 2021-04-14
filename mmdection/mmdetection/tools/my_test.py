from mmdet.apis import init_detector, inference_detector,show_result_pyplot
import numpy as np
import os
import cv2
import random
import mmcv
import time
import csv


config_file = 'configs/faster_rcnn/faster_rcnn_r50_fpn_1x_coco.py'
checkpoint_file = '/home/lywh/lywh-file-dir/code/contest/2021contest/underwater/newcode/mmdection/mmdetection/work_dirs/faster_rcnn_r101_fpn_1x_coco/epoch_26.pth'

# build the model from a config file and a checkpoint file
model = init_detector(config_file, checkpoint_file, device='cuda:0')

in_folder='/home/lywh/lywh-file-dir/data/underwater/test-A-image/'
out_folder='/home/lywh/lywh-file-dir/code/contest/2021contest/underwater/newcode/mmdection/mmdetection/work_dirs/faster_rcnn_r50_fpn_1x_coco/'



def get_confidence_from_result(filename,result):
    #print(filename)
    id2label={0:"holothurian",1:"echinus",2:"scallop",3:"starfish"}
    filename = filename[:-4]
    
    result_list = []
    for i in range(len(result)):
        #print(result[i])
        for j in range(len(result[i])):
            if result[i][j][4] < 0.5:
                continue
            temp_list = [id2label[i],str(filename)]
            temp_list.append(float(result[i][j][4]))
            temp_list.append(int(result[i][j][0]))
            temp_list.append(int(result[i][j][1]))
            temp_list.append(int(result[i][j][2]))
            temp_list.append(int(result[i][j][3]))
            result_list.append(temp_list)
    #result_list = [str(var) for var in result_list]
    #print(result_list)
    return result_list
    




if __name__=="__main__":
    if not os.path.exists(out_folder):
        os.makedirs(out_folder)
    file_list = os.listdir(in_folder)
    file_list.sort(key= lambda x:int(x[:-4]))
    csv_path = '/home/lywh/lywh-file-dir/code/contest/2021contest/underwater/newcode/mmdection/mmdetection/work_dirs/CSVDIR/'
    csv_name = "submit.csv"
    csv_file = open(os.path.join(csv_path,csv_name),"w",encoding='utf-8')
    csv_file = csv.writer(csv_file)
    csv_file.writerow(['name','image_id','confidence','xmin','ymin','xmax','ymax'])


    for file_name in file_list:
        img_path=os.path.join(in_folder,file_name)
        print(img_path)
        img=cv2.imread(img_path)
        # test a single image and show the results
        #img = 'demo/test.jpg'  # or img = mmcv.imread(img), which will only load it once
        #img=test_img
        result = inference_detector(model, img)
        result_list =  get_confidence_from_result(file_name,result)
        for row in result_list:
            #print(row)
            csv_file.writerow(row)

        # visualize the results in a new window
        #model.show_result(img, result)
        # or save the visualization results to image files
        #save_path=os.path.join(out_folder,file_name)
        #model.show_result(img, result, out_file=save_path)
        #show_result_pyplot(model, img, result)
