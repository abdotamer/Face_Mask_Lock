import cv2 as cv
import serial

Ard = serial.Serial("com6", 9600)

pathF = 'Cascade\haarcascade_frontalface_default.xml'
pathM = 'Cascade\haarcascade_mcs_mouth.xml'

cameraNo = 0  # CAMERA NUMBER

GREEN = (0, 255, 0)
RED = (0, 0, 255)

Scale = 1.4
neib = 2


cam = cv.VideoCapture(cameraNo)
cam.set(3, 640)
cam.set(4, 360)

casF = cv.CascadeClassifier(pathF)
casM = cv.CascadeClassifier(pathM)

while 1:
    Acs = "1\n"
    success, img = cam.read()
    if success:
        gr = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
        Faces = casF.detectMultiScale(gr, Scale, neib)
        for (x, y, w, h) in Faces:
            fc = gr[y: y + h + 20, x: x + w + 20]
            nw = int((w + 20) * 1.5)
            nh = int((h + 20) * 1.5)
            newFc = cv.resize(fc, (nw, nh), interpolation=cv.INTER_AREA)
            Mouths = casM.detectMultiScale(newFc, 1.3, 10)
            x2 = y2 = w2 = h2 = 0
            for(mx, my, mw, mh) in Mouths:
                x2 = max(x2, mx)
                y2 = max(y2, my)
                w2 = max(w2, mw)
                h2 = max(h2, mh)

            #cv.rectangle(img, (x2+x, y2+y), (x2 +x+ w2, y2+y + h2), (255, 0, 0), 2)
            if y2 > nh / 2.3:
                Acs = "0\n"
                cv.rectangle(img, (x, y), (x + w, y + h), RED, 2)
            else:
                cv.rectangle(img, (x, y), (x + w, y + h), GREEN, 2)
        cv.imshow("Camera", img)
        Ard.write(Acs.encode())
        print(Acs)
        if cv.waitKey(1) & 0xFF == ord('q'):
            break
    else:
        break