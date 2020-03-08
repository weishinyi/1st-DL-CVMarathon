#-------------------------------------------------
# file: convert_vocxml_to_yolofrmat.py
# date: 2020.03.05
# author: Nia
# description: 
#
# voc to yolo bbox轉換公式:
#    x = (xmin + (xmax-xmin)/2) * 1.0 / image_w
#    y = (ymin + (ymax-ymin)/2) * 1.0 / image_h
#    w = (xmax-xmin) * 1.0 / image_w
#    h = (ymax-ymin) * 1.0 / image_h
#
# yolo format:
# [classID] [obj Center in X] [obj Center in Y] [obj Width in X] [obj width in Y]
#    classID: 類別代碼
#    obj Center in X: 物件中心x位在整張圖片x的比例
#    obj Center in Y: 物件中心y位在整張圖片y的比例
#    obj Width in X: 物件寬度w佔整張圖片寬度的比例
#    obj width in Y: 物件長度h佔整張圖片長度的比例
#-------------------------------------------------

import os
import xml.etree.ElementTree as ET

classId_dict = {"kangaroo":0, "raccoon":1} 

def convert_vocxml_to_yoloformat(vocDir, yoloDir):

    # check dir exist
    isVocDirExist = os.path.exists(vocDir)
    if isVocDirExist == False:
        print('vocDir is NOT exist.')
    else:
        isYoloDirExist = os.path.exists(yoloDir)
        if isYoloDirExist == False:
            print('yoloDir is NOT exist.')
        else:
            print('vocDir: ', vocDir)
            print('yoloDir: ', yoloDir)

            #get xml file list
            xmlfileList = os.listdir(vocDir)
            xmlfileList = [elem for elem in xmlfileList if ('.xml' in elem)]
            
            totalNum = len(xmlfileList)
            print('Total number: ', totalNum)

            #loop
            cnt = 0
            for xmlFile in xmlfileList:
                if((cnt+1)%10) == 0:
                    print("process: ",(cnt+1),"/", totalNum)

                fileName = xmlFile.split('.')[0]
                xmlFilePath = os.path.join(vocDir, xmlFile)
                yoloFile = fileName + '.txt'
                yoloFilePath = os.path.join(yoloDir, yoloFile)
                
                #print("--- ",(cnt+1),"/", totalNum," ---")
                #print("vocxmlFile:",xmlFile)
                #print("yoloFile:",yoloFile)

                #open yolo file
                yolo_fp = open(yoloFilePath, "w")

                #read & parse xml file
                tree = ET.parse(xmlFilePath)
                root = tree.getroot()

                image_w = int(root.find('size').find('width').text)
                image_h = int(root.find('size').find('height').text)
                #print('img size(w,h):(', image_w,',', image_h,")")

                objCnt = 0
                for obj in root.iter('object'):

                    #get class id
                    objName = obj.find('name').text
                    objclassId = classId_dict[objName]
            
                    #get bbox 
                    xmin = int(obj.find('bndbox').find('xmin').text)
                    ymin = int(obj.find('bndbox').find('ymin').text)
                    xmax = int(obj.find('bndbox').find('xmax').text)
                    ymax = int(obj.find('bndbox').find('ymax').text)
                    objbbox = [xmin, ymin, xmax, ymax]
                    #print("[",objCnt,"] Name:",objName, ' classID:', objclassId," bbox:", objbbox)

                    #bbox convert
                    x = (xmin + (xmax-xmin)/2) * 1.0 / image_w
                    y = (ymin + (ymax-ymin)/2) * 1.0 / image_h
                    w = (xmax-xmin) * 1.0 / image_w
                    h = (ymax-ymin) * 1.0 / image_h

                    #wirte yolo file
                    outputLine = str(objclassId) + " " + str(x) + " " + str(y) + " " + str(w) + " " + str(h) +'\n'
                    yolo_fp.write(outputLine)

                    objCnt = objCnt +1
                yolo_fp.close()

                cnt = cnt + 1
                #if(cnt > 0):
                #    break



if __name__ == '__main__':
    annots_voc_dir = "kangaroo_raccoon_yolo_dataset/labels"
    annots_yolo_dir = "kangaroo_raccoon_yolo_dataset/Yolos"
    convert_vocxml_to_yoloformat(annots_voc_dir, annots_yolo_dir)
    