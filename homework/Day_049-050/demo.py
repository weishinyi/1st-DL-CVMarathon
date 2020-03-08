#-------------------------------------------------
# file: demo.py
# date: 2020.03.07
# author: Nia
# description: 使用yolov3對圖片/圖片集/影片做偵測
#-------------------------------------------------
import cv2
import numpy as np
import os

#---------------------------------------------------
model_weight = 'kangaroo_raccoon_yolo_dataset/cfg/weights/yolov3_last.weights'
model_cfg = 'kangaroo_raccoon_yolo_dataset/cfg/yolov3.cfg'
net = cv2.dnn.readNet(model_weight, model_cfg)

label_file = 'kangaroo_raccoon_yolo_dataset/cfg/obj.names'
classes = []

#load label list
with open(label_file, "r") as f:
    classes = [line.strip() for line in f.readlines()]
#print('label:',classes)

layer_names = net.getLayerNames()
output_layers = [layer_names[i[0] - 1] for i in net.getUnconnectedOutLayers()]
colors = np.random.uniform(0, 255, size=(len(classes), 3))
#-----------------------------------------------------------
def demo_img():
    
    # Loading image
    imgPath = 'test2.jpg'
    img = cv2.imread(imgPath)
    img = cv2.resize(img, None, fx=0.4, fy=0.4)
    height, width, channels = img.shape
    
    # Detecting objects
    blob = cv2.dnn.blobFromImage(img, 0.00392, (416, 416), (0, 0, 0), True, crop=False)
    net.setInput(blob)
    outs = net.forward(output_layers)
    #print('outs: ',outs)

    # Showing informations on the screen
    class_ids = []
    confidences = []
    boxes = []
    for out in outs:
        for detection in out:
            scores = detection[5:]
            class_id = np.argmax(scores)
            confidence = scores[class_id]
            if confidence > 0.5:
                # Object detected
                center_x = int(detection[0] * width)
                center_y = int(detection[1] * height)
                w = int(detection[2] * width)
                h = int(detection[3] * height)
                # Rectangle coordinates
                x = int(center_x - w / 2)
                y = int(center_y - h / 2)
                boxes.append([x, y, w, h])
                confidences.append(float(confidence))
                class_ids.append(class_id)

    # do nms
    indexes = cv2.dnn.NMSBoxes(boxes, confidences, 0.5, 0.4)
    
    # draw result 
    font = cv2.FONT_HERSHEY_PLAIN
    for i in range(len(boxes)):
        if i in indexes:
            x, y, w, h = boxes[i]
            label = str(classes[class_ids[i]])
            color = colors[i]
            cv2.rectangle(img, (x, y), (x + w, y + h), color, 2)
            cv2.putText(img, label, (x, y + 30), font, 1, color, 2)
         

    cv2.imshow("Image", img)
    cv2.waitKey(0)
#---
def demo_imgSet():
    
    imgDir = 'kangaroo_raccoon_yolo_dataset/images'
    imgNameList = os.listdir(imgDir)

    #loop
    for imgName in imgNameList:

        # Loading image
        imgPath = os.path.join(imgDir, imgName)
        img = cv2.imread(imgPath)
        img = cv2.resize(img, None, fx=0.4, fy=0.4)
        height, width, channels = img.shape
        
        # Detecting objects
        blob = cv2.dnn.blobFromImage(img, 0.00392, (416, 416), (0, 0, 0), True, crop=False)
        net.setInput(blob)
        outs = net.forward(output_layers)

        # Showing informations on the screen
        class_ids = []
        confidences = []
        boxes = []
        for out in outs:
            for detection in out:
                scores = detection[5:]
                class_id = np.argmax(scores)
                confidence = scores[class_id]
                if confidence > 0.5:
                    # Object detected
                    center_x = int(detection[0] * width)
                    center_y = int(detection[1] * height)
                    w = int(detection[2] * width)
                    h = int(detection[3] * height)
                    # Rectangle coordinates
                    x = int(center_x - w / 2)
                    y = int(center_y - h / 2)
                    boxes.append([x, y, w, h])
                    confidences.append(float(confidence))
                    class_ids.append(class_id)

        # do nms
        indexes = cv2.dnn.NMSBoxes(boxes, confidences, 0.5, 0.4)
        
        # draw result 
        font = cv2.FONT_HERSHEY_PLAIN
        for i in range(len(boxes)):
            if i in indexes:
                x, y, w, h = boxes[i]
                label = str(classes[class_ids[i]])
                color = (255,0,0)
                cv2.rectangle(img, (x, y), (x + w, y + h), color, 2)
                cv2.putText(img, label, (x, y + 30), font, 1, color, 2)
            

        cv2.imshow("Image", img)
        cv2.waitKey(0)
#---
def demo_video():
    #videoPath = 'videos/Raccoon.mp4'
    videoPath = 'videos/Kangaroo.mp4'
    cap = cv2.VideoCapture(videoPath)
    
    while(True):
        # get a frame
        ret, frame = cap.read()
        
        img = cv2.resize(frame, (640,360))
        img = cv2.resize(img, None, fx=0.4, fy=0.4)
        height, width, channels = img.shape
        
        # Detecting objects
        blob = cv2.dnn.blobFromImage(img, 0.00392, (416, 416), (0, 0, 0), True, crop=False)
        net.setInput(blob)
        outs = net.forward(output_layers)
        #print('outs: ',outs)

        # Showing informations on the screen
        class_ids = []
        confidences = []
        boxes = []
        for out in outs:
            for detection in out:
                scores = detection[5:]
                class_id = np.argmax(scores)
                confidence = scores[class_id]
                if confidence > 0.5:
                    # Object detected
                    center_x = int(detection[0] * width)
                    center_y = int(detection[1] * height)
                    w = int(detection[2] * width)
                    h = int(detection[3] * height)
                    # Rectangle coordinates
                    x = int(center_x - w / 2)
                    y = int(center_y - h / 2)
                    boxes.append([x, y, w, h])
                    confidences.append(float(confidence))
                    class_ids.append(class_id)

        # do nms
        indexes = cv2.dnn.NMSBoxes(boxes, confidences, 0.5, 0.4)
        
        # draw result 
        font = cv2.FONT_HERSHEY_PLAIN
        for i in range(len(boxes)):
            if i in indexes:
                x, y, w, h = boxes[i]
                label = str(classes[class_ids[i]])
                #color = colors[i]
                color = (255,0,0)
                cv2.rectangle(img, (x, y), (x + w, y + h), color, 2)
                cv2.putText(img, label, (x, y + 30), font, 2, color, 2)

        #cv2.imshow('frame', frame)
        cv2.imshow("Image", img)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
    
#-----------------------------------------------------------
if __name__ == '__main__':
    demo_img()
    #demo_imgSet()
    #demo_video()