from ultralytics import YOLO
import cv2
import math 
import serial 
import time 
import serial
import datetime

# ser = serial.Serial('COM7', 115200)  # Ganti 'COM3' dengan port yang sesuai dengan Arduino
# time.sleep(0.05)  # Tunggu beberapa detik untuk koneksi serial stabil

# def kirim_data(nilai1,nilai2,nilai3,nilai4):
#     data = str(nilai1) + ',' +str(nilai2)+ ',' +str(nilai3)+ ',' + str(nilai4) + '\n'
#     ser.write(data.encode())  # Kirim nilai sebagai string
#     # print("Data terkirim:", nilai)

# start webcam
cap = cv2.VideoCapture(0)
cap.set(3,640)
cap.set(4,480)

dcenter_x = 0
center_x1 = 0
center_y1 = 0
center_x2 = 0
center_y2 = 0

# model
model = YOLO("abu1.pt")
# model.export(format='onnx')
# int8=True

# object classes
classNames = ["Padi","Silo"]


while True:
    success, img = cap.read()
    img = cv2.flip(img,-1)
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
            
             # Calculate width and height of the bounding box
            


            # confidence
            confidence = math.ceil((box.conf[0]*100))/100
            print("Confidence --->",confidence)

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
            cv2.putText(img, str(fps), (1,40), font, fontScale, color, 2)
            
            


            if classNames[cls] == "Padi":
              
                center_x1 = int((x1 + x2) / 2)
                center_y1 = int((y1 + y2) / 2)
                
                if (center_x1==dcenter_x):
                    center_x1=0
                    
                dcenter_x=center_x1
                
                # kirim_data(center_x,center_y)
                # time.sleep(0.05)
                
            if classNames[cls]== "Silo":
                center_x2 = int((x1 + x2) / 2)
                center_y2 = int((y1 + y2) / 2)
                
            # kirim_data(center_x1,center_y1,center_x2,center_y2)
            data = f"{center_x1},{center_y1},{center_x2},{center_y2}\n"
            print(data)
                
    
    cv2.imshow('Webcam', img)
    if cv2.waitKey(1) == ord('q'):
        break


cap.release()
cv2.destroyAllWindows()

