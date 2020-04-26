import cv2
import numpy

#init camera
cap=cv2.VideoCapture(0)

face_cascade=cv2.CascadeClassifier("haarcascade_frontalface_alt.xml")

skip=0
face_data=[]
dataset_path='./data/'
file_name=input("Enter the name of the person : ")


while True:
    ret,frame=cap.read()
    
    if ret==False:
        continue

#converting the image into gray scale to save memory
    gray_frame=cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)


    faces=face_cascade.detectMultiScale(frame,1.3,5)

# sorting the faces on the frame to get the largest face
    faces=sorted(faces,key=lambda f:f[2]*f[3])
    
# picking the largest face according to area according to area(f[2]*f[3])
    for face in faces[-1:]:
        x,y,w,h=face
        cv2.rectangle(frame,(x,y),(x+w,y+h),(0,255,255),2)

        #crope the required part of frame i.e. face with 10 extra padding
        offset=10

        face_section=frame[y-offset:y+h+offset,x-offset:x+w+offset]
        face_section=cv2.resize(face_section,(100,100))

        cv2.imshow("face section",face_section)
        
        skip+=1
        if skip%10==0:
            face_data.append(face_section)
            print(len(face_data))


    cv2.imshow("video frame",frame)
    
    
    key_pressed=cv2.waitKey(1) & 0xFF
    if key_pressed==ord('q'):
        break

#convert our face list array into numpy array
face_data=numpy.asarray(face_data)
face_data=face_data.reshape((face_data.shape[0],-1))
print(face_data.shape)

#save this data into file system
numpy.save(dataset_path+file_name+'.npy',face_data)
print("data successfully saved at"+dataset_path+file_name+'.npy')

cap.release()
cv2.destroyAllWindows()