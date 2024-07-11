import cv2

cam =  cv2.VideoCapture(1)
cam.set(3,1280)
cam.set(4,720)


while(1):
    ret,frame = cam.read()
    
    cv2.imshow("kamera",frame)
    
    k= cv2.waitKey(1) & 0xff
    
    if k==ord('q'):
        break
    
cam.release()
cv2.destroyAllWindows()