import cv2 as cv
import numpy as np

#reading the video feed
capture = cv.VideoCapture(2)
capture.set(cv.CAP_PROP_BUFFERSIZE, 1)



while True:
 

    isTrue, frame = capture.read()
    if isTrue: 
        # median blur to remove salt and pepper noise
        blur = cv.medianBlur(frame,11)
        # convert to grayscale for thresholding
        gray = cv.cvtColor(blur, cv.COLOR_BGR2GRAY)
        # converting image to lab colorspace
        lab  = cv.cvtColor(blur, cv.COLOR_BGR2LAB)
        # splitting lab colorspace for applying histogram equalisation on L channel
        l, a, b = cv.split(lab)
        l = cv.equalizeHist(l)

        lab = cv.merge((l,a,b))

        
        #applying adaptive threshold
        th1 = cv.adaptiveThreshold(gray, 255, cv.ADAPTIVE_THRESH_GAUSSIAN_C, cv.THRESH_BINARY, 11, 3) 
        
        #lab values
        l_b = np.array([124, 70, 153])
        u_b = np.array([255, 124, 255])
        
        #applying img proc techniques to refine mask
        mask = cv.inRange(lab, l_b, u_b)    
  
    
        mask = cv.erode(mask, None, iterations=7)
        mask = cv.dilate(mask, None, iterations=5)
        mask = cv.bilateralFilter(mask, 9, 75, 75)

     
        mask = cv.bitwise_and(mask, th1)
        res = cv.bitwise_and(frame, frame, mask=mask)
      

        #hough circles
        circles = cv.HoughCircles(mask, cv.HOUGH_GRADIENT, 1.6 , 100,  param1 = 50, param2 = 35 , minRadius = 15, maxRadius = 200)
       

        if circles is not None:
            #convert (x,y,r) into integers
            circles = np.round(circles[0, :]).astype("int")
            for (x,y,r) in circles:
                cv.circle(frame, (x,y), r, (255,0,0), 3)
                cv.circle(frame, (x,y), 3, (255,0,0), -1)
                cv.putText(frame, "Tennis Ball", (int(x), int(y) + 4), cv.FONT_HERSHEY_SIMPLEX, 1, (0,255,0), 2 )
        
        #showing the frames
        cv.imshow("mask", mask)
        cv.imshow("feed", frame)

    
    
 
        #press q to exit 
        if cv.waitKey(1) == ord("q"):
            break
    else:
        break



#to release the camera and close all windows
capture.release()
cv.destroyAllWindows()
