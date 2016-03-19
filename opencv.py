import cv2
import os,numpy
from PIL import Image

labels=[]
images=[]

def rotateImage(image, angle):
  # image_center = tuple(numpy.array(image.shape)/2)
  (h, w) = image.shape[:2]
  center = (w / 2, h / 2)
  rot_mat = cv2.getRotationMatrix2D(center=center,angle=angle,scale=1.0)
  result = cv2.warpAffine(image, rot_mat, (w, h))
  return result


face_cascadePath = "haarcascade_frontalface_default.xml"
eyes_cascadePath= "haarcascade_eye.xml"
faceCascade = cv2.CascadeClassifier(face_cascadePath)
eyes_cascade= cv2.CascadeClassifier(eyes_cascadePath)
recognizer = cv2.createLBPHFaceRecognizer()
# image_pil = Image.open('test/test1.jpg').convert('L')
# img= numpy.array(image_pil, 'uint8')

image_paths = []

for f in os.listdir('subjects'):
    if f.endswith('.jpg'):
        image_paths.append('subjects/'+f+';'+'1')
        print f

for path in image_paths:
    path,label=path.split(';')
    img = cv2.imread(path)
    img =cv2.resize(img,(0,0),fx=0.2,fy=0.2)
    img= rotateImage(img,-90)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = faceCascade.detectMultiScale(gray, 1.3, 5)
    for (x,y,w,h) in faces:
        cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,0),2)
        roi_gray = gray[y:y+h, x:x+w]
        roi_color = img[y:y+h, x:x+w]
        images.append(gray[y: y + h, x: x + w])
        labels.append(int(label))
        # cv2.imshow("Adding faces to traning set...", gray[y: y + h, x: x + w])
        # cv2.imshow('img',img)
        # cv2.waitKey(50)
# cv2.destroyAllWindows()
recognizer.train(images, numpy.array(labels))


img = cv2.imread('test/test7.jpg')
img =cv2.resize(img,(0,0),fx=0.2,fy=0.2)
img= rotateImage(img,-90)
cv2.imshow('load test',img)
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
faces = faceCascade.detectMultiScale(gray, 1.3, 5)
print faces
for (x, y, w, h) in faces:
    cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,0),2)
    roi_gray = gray[y:y+h, x:x+w]
    roi_color = img[y:y+h, x:x+w]
    predicted,conf=recognizer.predict(roi_gray)
    print predicted,conf
    cv2.imshow("Predicting...", img)
cv2.waitKey(5000)
cv2.destroyAllWindows()



# # paths=open('faces.csv')
# # paths.close()
# # paths=open('faces.csv')
# recognizer.save('train.yml')
# recognizer.load('train.yml')
# for path in paths:
#     path,label=path.split(';')
#     img = cv2.imread(path,0)
#     faces = faceCascade.detectMultiScale(img)
#     for (x, y, w, h) in faces:
#         predicted,conf=recognizer.predict(img[y: y + h, x: x + w])
#         print predicted,conf
#         cv2.imshow("Predicting...", img[y: y + h, x: x + w])
#         cv2.waitKey(5000)
# cv2.destroyAllWindows()
__author__ = 'gaurav'
