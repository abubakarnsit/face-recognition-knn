import numpy
import cv2
import os

def distance(v1,v2):
    return numpy.sqrt(((v1-v2)**2).sum())


def knn(train,test,k=5):
    dist=[]

    for i in range(train.shape[0]):	
     #get the vector and label
        ix=train[i,:-1]
        iy=train[i,-1]
         #sort based on distance from test point
        d=distance(test,ix)
        dist.append([d,iy])
    dk=sorted(dist,key=lambda x: x[0])[:k]
    #retrieve only the labels
    labels=numpy.array(dk)[:,-1]

    #get frequencies of each label
    output=numpy.unique(labels,return_counts=True)

    #find max frequency and corresponding label
    index=numpy.argmax(output[1])
    return output[0][index]

#initialise camera
cap=cv2.VideoCapture(0)

#face detection
face_cascade=cv2.CascadeClassifier("haarcascade_frontalface_alt.xml")

skip=0
dataset_path='./data/'


face_data=[]
labels=[]

#labels for given file
class_id=0

#mapping between id and name
names={}

#data preperation
for fx in os.listdir(dataset_path):
    if fx.endswith('.npy'):
        #mapping between class_id and name
        names[class_id]=fx[:-4]
        print("loaded   "+fx)
        data_item=numpy.load(dataset_path+fx)
        face_data.append(data_item)

        target=class_id*numpy.ones((data_item.shape[0],))
        class_id+=1
        labels.append(target)

face_dataset=numpy.concatenate(face_data,axis=0)
face_labels=numpy.concatenate(labels,axis=0).reshape((-1,1))

print(face_dataset.shape)
print(face_labels.shape)

trainset=numpy.concatenate((face_dataset,face_labels),axis=1)
print(trainset.shape)


#testing 
while True:
    ret,frame=cap.read()

    if ret==False:
        continue

    faces=face_cascade.detectMultiScale(frame,1.3,5)

    for face in faces:
        x,y,w,h=face

        #getting the region of frame in which face is present
        offset=10
        face_section=frame[y-offset:y+h+offset,x-offset:x+w+offset]
        face_section=cv2.resize(face_section,(100,100))

        #predicted label(out)
        out=knn(trainset,face_section.flatten())

        #display the name on the screen and rectangle around it
        pred_name=names[int(out)]
        cv2.putText(frame,pred_name,(x,y-10),cv2.FONT_HERSHEY_SIMPLEX,1,(255,0,0),2,cv2.LINE_AA)
        cv2.rectangle(frame,(x,y),(x+w,y+h),(0,255,255),2)


    #showing the image
    cv2.imshow("faces",frame)

    key=cv2.waitKey(1) & 0xFF
    if key==ord('q'):
        break


cap.release()
cv2.destroyAllWindows()

