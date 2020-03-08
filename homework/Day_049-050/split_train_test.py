#-------------------------------------------------
# file: split_train_test.py
# date: 2020.02.05
# author: Nia
# description: 用來切分train/test.txt
#-------------------------------------------------
import os
import random

#set param
train_percent = 0.8 # the scale of train set

# set your path
imgDirPath = 'kangaroo_raccoon_yolo_dataset/images'
yoloDirpath = 'kangaroo_raccoon_yolo_dataset/Yolos'
savefilePath = 'kangaroo_raccoon_yolo_dataset/cfg'

#
imgList = os.listdir(imgDirPath)
imgNumber = len(imgList)
list = range(imgNumber)
tr = int(imgNumber*train_percent)
train = random.sample(list, tr)

print("train size",tr)
ftrain = open(os.path.join(savefilePath,'train.txt'), 'w')
ftest = open(os.path.join(savefilePath,'test.txt'), 'w')

for i in list:
    name = imgList[i][:-4]+'\n'
    imgName = imgList[i] + '\n'
    #imgPath = os.path.join(imgDirpath, imgName)
    imgPath = yoloDirpath + "/" + imgName
    if i in train:
        ftrain.write(imgPath)
    else:
        ftest.write(imgPath)

ftrain.close()
ftest .close()

print('gen the files in:',savefilePath)