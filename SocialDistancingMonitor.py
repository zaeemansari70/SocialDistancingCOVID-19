## CODE CITATIONS
## https://www.pyimagesearch.com/2015/11/09/pedestrian-detection-opencv/
## https://automaticaddison.com/how-to-detect-pedestrians-in-images-and-video-using-opencv/



## SOCIAL DISTANCING MONITOR - ITERATION 1

import cv2
import numpy as np

#Creating a variable for a HOG Featur Descriptor
hog = cv2.HOGDescriptor()    

#Setting Hog variable to SVM automated object detection with the parameter
#that allows it to detect human beings in an image
hog.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector())


#Reading the input image into a variable
img = cv2.imread(r'path')


#Using "detectMultiScale()" fucntion of the HOG descriptor to detect human beings 
#And Populating the coordinates of all the bouding boxes detected by the function 
#into an array called "bounding_boxes"
(bounding_boxes, weights) = hog.detectMultiScale (img, winStride=(2,2), padding=(4,4), scale=1.01)


#Drawing a Blue Bouding rectangle on each object detected by HOGDescriptor
for (x,y,w,h) in bounding_boxes:
    cv2.rectangle(img, (x,y),(x+w,y+h), (255,0,0),1)


cv2.imshow("Original Image",img)
cv2.waitKey()



#Creating a boolean array that distinguishes Overlapping rectangles from Non-overlapping ones
##If for example, our array is equal to [1,1,0,0]. This means that the rectangles stored at
#index 0, and index 1 are overlapping. While, rectangles ar indexes 2, and 3 are not overlapping.

Overlapping_boxes = np.zeros(len(bounding_boxes))

#Boolean used to detect overlapping rectangles
overlap =True

#A loop that runs for the length of our "Bounding_boxes" array
for i in range(0, len(bounding_boxes)-1): 
    
    #Bounding_Boxes Sample Array
    #[[ x   y    width  height]]
    #[[120  220   80     370]]
    
    #Top left coordinates of Rectangle 1
    R1_x1= bounding_boxes[i][0]
    R1_y1= bounding_boxes[i][1]

    #Bottom right coordinates of rectangle 1
    #Add width and x to get bottom right x coordinate
    #Add height and y to get bottom right y coordinate
    R1_x2 = R1_x1 + bounding_boxes[i][2]
    R1_y2 = R1_y1 + bounding_boxes[i][3]



    for j in range(i+1,len(bounding_boxes)):

        #Top left coordinates of rectangle 2
        R2_x1= bounding_boxes[j][0]
        R2_y1= bounding_boxes[j][1]

        #Bottom right coordinates of rectangle 2
        R2_x2 = R2_x1 + bounding_boxes[j][2]
        R2_y2 = R2_y1 + bounding_boxes[j][3]


        #Comparing Coordinates of rectangle 1 and rectangle 2 to detect overlap
        if ((R1_x1 >= R2_x2) or (R2_x1 >= R1_x2)):
            overlap = False

        elif ((R1_y1 >= R2_y2) or (R2_y1 >= R1_y2)):
            overlap = False

        #If an overlap is detected, set the boolean value of the corresponding rectangle to True.
        #Which is an idication that we need to show a safety alert for that human being.
        if(overlap==True):
            Overlapping_boxes[i]=1
            Overlapping_boxes[j]=1


        overlap=True


#Drawing a Red Bouding Box for Humans that are violating Social Distancing Rules
#And Drawing a Green Bounding Box for Humans that are safe.
for i in range(0,len(Overlapping_boxes)):
    x = bounding_boxes[i][0]
    y= bounding_boxes[i][1]
    x2 = x + bounding_boxes[i][2]
    y2 = y + bounding_boxes[i][3]

    if(Overlapping_boxes[i]==1):
        cv2.rectangle(img, (x,y),(x2,y2), (0,0,255),1)
        cv2.putText(img, 'Alert', (x,y), cv2.FONT_HERSHEY_COMPLEX, 0.8, (0,0,255), 2, cv2.LINE_AA)

    else:
        cv2.rectangle(img, (x,y),(x2,y2), (0,255,0),1)
        cv2.putText(img, 'Safe', (x,y), cv2.FONT_HERSHEY_COMPLEX, 0.8, (0,255,0), 2, cv2.LINE_AA)
        

cv2.imshow('Social Distancing Monitor', img)
cv2.waitKey(0)




