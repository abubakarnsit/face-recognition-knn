import cv2
cap=cv2.VideoCapture(0)
while True:
    ret,frame=cap.read()
    gray_frame=cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
    if ret==False:
        continue
    key_pressed=cv2.waitKey(1) & 0xFF
    if key_pressed==ord('q'):
        break
    cv2.imshow("video frame",frame)
    cv2.imshow("grey frame",gray_frame)

cap.release()
cv2.destrouAllWindowns()