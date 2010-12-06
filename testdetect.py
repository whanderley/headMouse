import sys
from opencv.cv import *
from opencv.highgui import *
import pymouse

 
def detect(image):
    image_size = cvGetSize(image)
 
    # create grayscale version
    grayscale = cvCreateImage(image_size, 8, 1)
    
    cvCvtColor(image, grayscale, CV_BGR2GRAY)
 
    # create storage
    storage = cvCreateMemStorage(0)
    cvClearMemStorage(storage)
    # equalize histogram
    cvEqualizeHist(grayscale, grayscale)
        
    # detect object
    cascade = cvLoadHaarClassifierCascade(
    '/usr/share/opencv/haarcascades/haarcascade_frontalface_default.xml', 
    cvSize(1,1))
    faces = cvHaarDetectObjects(grayscale, cascade, storage, 2, 2, 
    CV_HAAR_DO_CANNY_PRUNING, cvSize(100,100))
    if faces.total == 1:
        for i in faces:
            #_x = abs((screen_size[0]*(((i.x+96)/448.)-3./14)))
            _x = screen_size[0]*((17/14.)-(i.x+96)/448.)   
            mouse.move(_x, (screen_size[1]*(((i.y+96)/288.)-1./3)))
            cvRectangle(image, cvPoint( (i.x), (i.y)),
                         cvPoint((i.x + i.width), (i.y + i.height)),
                         CV_RGB(0, 255, 0), 3, 8, 0)                         
                           
    return faces.total
 
if __name__ == "__main__":
    k = 'u'
 
    print "Press ESC to exit ..."
 
    # create windows
    cvNamedWindow('Camera') 

    capture = cvCreateCameraCapture(0)  
    cvSetCaptureProperty(capture, CV_CAP_PROP_FRAME_WIDTH, 640)
    cvSetCaptureProperty(capture, CV_CAP_PROP_FRAME_HEIGHT, 480)   
    if not capture: # check if capture device is OK
        print "Error opening capture device"
        sys.exit(1) 
    mouse = pymouse.PyMouse()  
    screen_size = mouse.screen_size()
    while 1:
        frame = cvQueryFrame(capture)
        if frame is None:
            break
 
        # face detection
        total = detect(frame) 
        if total == 1:
            break
         # display webcam image
        cvShowImage('Camera', frame)    
 
        # handle events
        k = cvWaitKey(10)        
    ultimo = 6 
    while k <> 'q':
        # do forever
 
        # capture the current frame
        frame = cvQueryFrame(capture)
        if frame is None:
            break
        
        # face detection
        total = detect(frame) 
        if total == 0  and ultimo > 5:
            ultimo = 0
        elif ultimo == 3:
            position = mouse.position()
            mouse.click(position[0], position[1])   
        ultimo += 1     
        # display webcam image
        cvShowImage('Camera', frame)
 
        # handle events
        k = cvWaitKey(15)
