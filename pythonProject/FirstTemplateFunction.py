def firstTemplateList(img,smallTemp,bigTemp,p1,p2):
    import cv2
    import numpy as np
    try:
        img_c = img.copy()
        img = cv2.GaussianBlur(img, (13, 13), -1)
        hsvB = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        lowerBlue = np.array([100, 0, 0])
        upperBlue = np.array([125, 255, 255])
        maskBlue = cv2.inRange(hsvB, lowerBlue, upperBlue)
        outputBlue = cv2.bitwise_and(img, img, mask=maskBlue)
        grblue = cv2.cvtColor(outputBlue, cv2.COLOR_BGR2GRAY)

        circles = cv2.HoughCircles(grblue, cv2.HOUGH_GRADIENT, 1, 20,
                                   param1=p1, param2=p2, minRadius=19, maxRadius=30)
        detectedCircles = np.uint16(np.around(circles))
        #print(detectedCircles.shape)

        temp1 = np.int16(smallTemp/2)
        temp2 = np.int16(bigTemp/2)


        xBall1 = detectedCircles[0, 0, 0]
        yBall1 = detectedCircles[0, 0, 1]
        xBall2 = detectedCircles[0, 1, 0]
        yBall2 = detectedCircles[0, 1, 1]
        xBall3 = detectedCircles[0, 2, 0]
        yBall3 = detectedCircles[0, 2, 1]

        cropimg1 = img_c[yBall1 - temp1:yBall1 + temp1, xBall1 - temp1:xBall1 + temp1]
        #cv2.imshow("cropimg1",cropimg1), cv2.waitKey(0), cv2.destroyAllWindows()
        cropimg2 = img_c[yBall2 - temp1:yBall2 + temp1, xBall2 - temp1:xBall2 + temp1]
        #cv2.imshow("cropimg2", cropimg2), cv2.waitKey(0), cv2.destroyAllWindows()
        cropimg3 = img_c[yBall3 - temp1:yBall3 + temp1, xBall3 - temp1:xBall3 + temp1]
        #cv2.imshow("cropimg3", cropimg3), cv2.waitKey(0), cv2.destroyAllWindows()

        cropimg11 = img_c[yBall1 - temp2:yBall1 + temp2, xBall1 - temp2:xBall1 + temp2]
        cropimg22 = img_c[yBall2 - temp2:yBall2 + temp2, xBall2 - temp2:xBall2 + temp2]
        cropimg33 = img_c[yBall3 - temp2:yBall3 + temp2, xBall3 - temp2:xBall3 + temp2]

    except:
        print("problem: Gene yapamadık, gine olmadı, yine canımız sıkıldı")

    return cropimg1, cropimg2, cropimg3, cropimg11, cropimg22, cropimg33

#img = cv2.imread("data/salon.jpg")
#a = firstTemplateList(img,44,90,40,14)
#smallTemplate1 = a[0]
#smallTemplate2 = a[1]
#smallTemplate3 = a[2]
#bigTemplate1 = a[3]
#bigTemplate2 = a[4]
#bigTemplate3 = a[5]

#cv2.imshow("original", img)
#cv2.imshow("temp1", a[0])
#cv2.imshow("temp2", a[1])
#cv2.imshow("temp3", a[2])
#cv2.imshow("temp4", a[3])
#cv2.imshow("temp5", a[4])
#cv2.imshow("temp6", a[5])

#cv2.waitKey(0)
#cv2.destroyAllWindows()
