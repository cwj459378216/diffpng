import cv2
import imutils 
import numpy as np


def diffpng(origin, new, diffName):
    #get the images you want to compare.
    original = cv2.imread(origin)
    new = cv2.imread(new)

    if str(original.shape) != str(new.shape):
        createDiffpng(original, new, diffName)
        return
    difference = cv2.subtract(original, new)
    result = not np.any(difference) #if difference is all zeros it will return False
    
    if result is True:
        print(diffName + "-> 两张图片一样")
    else:
        createDiffpng(original, new, diffName)

def createDiffpng(original, new, diffName):
    #  cv2.imwrite("result.jpg", difference)
        #resize the images to make them small in size. A bigger size image may take a significant time
        #more computing power and time
        original = imutils.resize(original, height = 600)
        new = imutils.resize(new, height = 600)

        #create a copy of original image so that we can store the
        #difference of 2 images in the same on
        diff = original.copy()
        cv2.absdiff(original, new, diff)


        #converting the difference into grayscale images
        gray = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)

        #increasing the size of differences after that we can capture them all
        for i in range(0, 3):
            dilated = cv2.dilate(gray.copy(), None, iterations= i+ 1)

        #threshold the gray image to binary it. Anything pixel that has
        #value higher than 3 we are converting to white
        #(remember 0 is black and 255 is exact white)
        #the image is called binarised as any value lower than 3 will be 0 and
        # all of the values equal to and higher than 3 will be 255
        (T, thresh) = cv2.threshold(dilated, 3, 255, cv2.THRESH_BINARY)

        # now we have to find contours in the binarized image
        cnts = cv2.findContours(thresh, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
        cnts = imutils.grab_contours(cnts)

        for c in cnts:
            # nicely fiting a bounding box to the contour
            (x, y, w, h) = cv2.boundingRect(c)
            cv2.rectangle(new, (x, y), (x + w, y + h), (0, 255, 0), 2)

        #remove comments from below 2 lines if you want to
        #for viewing the image press any key to continue
        #simply write the identified changes to the disk
        cv2.imwrite("./pic/diff/" + diffName, new)
        print (diffName + "-> 两张图片不一样")
