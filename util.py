import pyqrcode,base64,os
import cv2,numpy

labels=[]
images=[]
face_cascadePath = "haarcascade_frontalface_default.xml"
faceCascade = cv2.CascadeClassifier(face_cascadePath)
recognizer = cv2.createLBPHFaceRecognizer()
image_paths = []


def train():
    paths=open("faces.csv","r")
    for path in paths:
        print path
        path,label=path.split(';')
        print path
        img = cv2.imread(path)
        img =cv2.resize(img,(0,0),fx=0.2,fy=0.2)
        img= rotateImage(img,90)
        cv2.imshow("after rotation",img)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        faces = faceCascade.detectMultiScale(gray, 1.3, 5)
        for (x,y,w,h) in faces:
            print x,y,w,h
            cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,0),2)
            roi_gray = gray[y:y+h, x:x+w]
            roi_color = img[y:y+h, x:x+w]
            images.append(gray[y: y + h, x: x + w])
            labels.append(int(label))
            cv2.imshow("Adding faces to traning set...", gray[y: y + h, x: x + w])
            cv2.waitKey(5000)
        cv2.destroyAllWindows()
    recognizer.train(images, numpy.array(labels))
    recognizer.save('trained_set.yml')


def rotateImage(image, angle):
  # image_center = tuple(numpy.array(image.shape)/2)
  (h, w) = image.shape[:2]
  center = (w / 2, h / 2)
  rot_mat = cv2.getRotationMatrix2D(center=center,angle=angle,scale=1.0)
  result = cv2.warpAffine(image, rot_mat, (w, h))
  return result

def face_rec(image,valid_label):
    recognizer.load('trained_set.yml')
    img = cv2.imread('test/'+image)
    img =cv2.resize(img,(0,0),fx=0.2,fy=0.2)
    img= rotateImage(img,90)
    cv2.imshow("after rotation",img)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = faceCascade.detectMultiScale(gray, 1.3, 5)
    print faces
    for (x, y, w, h) in faces:
        cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,0),2)
        roi_gray = gray[y:y+h, x:x+w]
        roi_color = img[y:y+h, x:x+w]
        predicted,conf=recognizer.predict(roi_gray)
        print predicted,conf
        if conf==-1 or predicted != int(valid_label):
            cv2.imshow("Not Allowed",img)
        elif predicted==int(valid_label):
            cv2.imshow("Allowed",img)
    cv2.waitKey(5000)
    cv2.destroyAllWindows()


def generate(data):
    data=str(data)
    code=pyqrcode.create(data)
    image="temp.png"
    code.png(image,scale=10)
    encoded = base64.b64encode(open(image, "rb").read())
    os.remove("temp.png")
    return encoded


# def authenticate(id):
#     try:
#         id=str(id)
#         print id
#         monument=mongo.db.monuments.find_one({"_id":ObjectId(id)})
#         if monument is not None:
#             data={}
#             data['authUrl']=monument['authUrl']
#             data['twoFactor']=monument['twoFactor']
#             data['params']=monument['params']
#             code=pyqrcode.create(json.dumps(data))
#             image=id+".png"
#             code.png(image,scale=10)
#             os.rename(image,"static/"+image)
#             return render_template("scan.html",image=image)
#     except Exception as e:
#         print "here"
#         return str(e)

# train()
face_rec("test9.jpg",1)
face_rec("test10.jpg",0)
__author__ = 'gaurav'
