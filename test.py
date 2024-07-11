from ultralytics import YOLO
import cv2
import math 
import serial 
import time 
import serial
import datetime
import torch


# arduino = serial.Serial(port='COM100', baudrate=115200, timeout=.1)

# def send_data(value):
#     arduino.write(str(value).encode())
#     time.sleep(0.05)
#     data = arduino.readline().decode().strip()
#     return data

# start webcam
cap = cv2.VideoCapture(1)
# cap.set(3, 640)
# cap.set(4, 480)

center = 640/2

# model
model = YOLO("yolo-Weights/yolov8n.pt")
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')


# object classes
classNames = ["person", "bicycle", "car", "motorbike", "aeroplane", "bus", "train", "truck", "boat",
              "traffic light", "fire hydrant", "stop sign", "parking meter", "bench", "bird", "cat",
              "dog", "horse", "sheep", "cow", "elephant", "bear", "zebra", "giraffe", "backpack", "umbrella",
              "handbag", "tie", "suitcase", "frisbee", "skis", "snowboard", "sports ball", "kite", "baseball bat",
              "baseball glove", "skateboard", "surfboard", "tennis racket", "bottle", "wine glass", "cup",
              "fork", "knife", "spoon", "bowl", "banana", "apple", "sandwich", "orange", "broccoli",
              "carrot", "hot dog", "pizza", "donut", "cake", "chair", "sofa", "pottedplant", "bed",
              "diningtable", "toilet", "tvmonitor", "laptop", "mouse", "remote", "keyboard", "cell phone",
              "microwave", "oven", "toaster", "sink", "refrigerator", "book", "clock", "vase", "scissors",
              "teddy bear", "hair drier", "toothbrush"
              ]


while True:
    success, img = cap.read()
    results = model(img, stream=True)
    start = datetime.datetime.now()

    
    # coordinates
    for r in results:
        boxes = r.boxes
        

        for box in boxes:
            # bounding box
            x1, y1, x2, y2 = box.xyxy[0]
            x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2) # convert to int values
            #print(x1) 

            # put box in cam
            cv2.rectangle(img, (x1, y1), (x2, y2), (255, 0, 255), 3)

            # confidence
            confidence = math.ceil((box.conf[0]*100))/100
            #print("Confidence --->",confidence)

            # class name
            cls = int(box.cls[0])
            #print("Class name -->", classNames[cls])

            # object details
            org = [x1, y1]
            font = cv2.FONT_HERSHEY_SIMPLEX
            fontScale = 1
            color = (255, 0, 0)
            thickness = 2
            cv2.putText(img, classNames[cls], org, font, fontScale, color, thickness)
            end = datetime.datetime.now()
            total = (end - start).total_seconds()
            fps = f"fps: {1 / total:.2f}"
            print (fps)


            if classNames[cls] == "person":
                sudut= 0
                center_x = int((x1 + x2) / 2)
                if center_x < 10:
                    sudut = 1
                elif 10 <= center_x < 20:
                    sudut = 2
                elif 20 <= center_x < 30:
                    sudut = 3
                print("sudut: ", sudut)
                # response = send_data(x1)
            
    
    cv2.imshow('Webcam', img)
    if cv2.waitKey(1) == ord('q'):
        break


cap.release()
cv2.destroyAllWindows()

