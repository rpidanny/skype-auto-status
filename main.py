import cv2
import sys
import dbus
import time

cascPath = "face.xml" 
#|| sys.argv[1]
faceCascade = cv2.CascadeClassifier(cascPath)

video_capture = cv2.VideoCapture(0)

bus = dbus.SessionBus()

proxy = bus.get_object('com.Skype.API', '/com/Skype')

proxy.Invoke('NAME skype_status.py')
proxy.Invoke('PROTOCOL 2')

dCount =0
nCount =0
flag = False
while True:
    # Capture frame-by-frame
    ret, frame = video_capture.read()

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    faces = faceCascade.detectMultiScale(
        gray,
        scaleFactor=1.1,
        minNeighbors=5,
        minSize=(30, 30),
        flags=cv2.CASCADE_SCALE_IMAGE
    )

    if len(faces):
        dCount+=1
        nCount = 0
        if(dCount>5 and flag==False):
            proxy.Invoke("SET USERSTATUS Online")
            proxy.Invoke("""SET PROFILE MOOD_TEXT "Auto Status Changed : Available  :- http://gitlabs.javra.com/abhishek/skype-auto-status" """)
            print "face Detected"
            dCount = 0
            flag = True
        else:
            flag = False
        #print len(faces)
        for (x, y, w, h) in faces:
            cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
    else:
        dCount = 0
        nCount+=1
        if(nCount>10 and flag==False):
            print "No Face"
            proxy.Invoke("SET USERSTATUS Away")
            proxy.Invoke("""SET PROFILE MOOD_TEXT "Auto Status Changed : Away  :- http://gitlabs.javra.com/abhishek/skype-auto-status" """)
            nCount = 0
            flag=True
        else:
            flag=False

    # Display the resulting frame
    #cv2.imshow('Video', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    time.sleep(1)

# When everything is done, release the capture
video_capture.release()
cv2.destroyAllWindows()
