import numpy as np
import math
import cv2
from fish_eye_correct import fish_eye_correct

def firstTemp(img,frame, smallTemp, bigTemp):
    def findYellowCenter(img):
        threshold = 60
        yavgX = 0
        yavgY = 0
        ycount = 0
        #Yellow = [30, 169, 255]
        boundaries_yellow = [([30, 150, 150], [35, 255, 255])]
        for (lower, upper) in boundaries_yellow:
            low_boundary_yellow = np.array(lower, dtype="uint8")
            up_boundary_yellow = np.array(upper, dtype="uint8")
            mask_yellow = cv2.inRange(img, low_boundary_yellow, up_boundary_yellow)

        output = cv2.bitwise_and(img, img, mask=mask_yellow)
        cv2.imshow('final', output) , cv2.waitKey(0), cv2.destroyAllWindows()
        yellow_arr = np.where(mask_yellow == 255)
        print("yellow",yellow_arr)
        for y in (yellow_arr[0]):
            for x in (yellow_arr[1]):
                #b1 = img[y, x, 0]
                #g1 = img[y, x, 1]
                #r1 = img[y, x, 2]
                #Diff = math.sqrt((b1 - Yellow[0]) * (b1 - Yellow[0]) +
                                 #(g1 - Yellow[1]) * (g1 - Yellow[1]) +
                                 #(r1 - Yellow[2]) * (r1 - Yellow[2]))
                #if (Diff < threshold):
                    #print("yellow girdim")
                yavgX += x
                yavgY += y
                ycount += 1
        YcenterX = yavgX / ycount
        YcenterY = yavgY / ycount
        print(YcenterX,YcenterY)
        return YcenterX, YcenterY

    def findRedCenter(img):
        #threshold = 50
        ravgX = 0
        ravgY = 0
        rcount = 0
        #Red = [10, 240, 245]

        boundaries_red = [([0, 120, 70], [10, 255, 255])]
        for (lower,upper) in boundaries_red:
            low_boundary_red = np.array(lower,dtype="uint8")
            up_boundary_red = np.array(upper,dtype="uint8")
            mask_red_1 = cv2.inRange(img,low_boundary_red,up_boundary_red)

        boundaries_red = [([170, 120, 70], [180, 255, 255])]
        for (lower, upper) in boundaries_red:
            low_boundary_red = np.array(lower, dtype="uint8")
            up_boundary_red = np.array(upper, dtype="uint8")
            mask_red_2 = cv2.inRange(img, low_boundary_red, up_boundary_red)

        mask_red = mask_red_1+mask_red_2
        output = cv2.bitwise_and(img, img, mask=mask_red)
        cv2.imshow('final', output), cv2.waitKey(0), cv2.destroyAllWindows()
        red_arr = np.where(mask_red==255)
        print("red ",red_arr)
        for y in (red_arr[0]):
            for x in (red_arr[1]):
                #b1 = img[y, x, 0]
                #g1 = img[y, x, 1]
                #r1 = img[y, x, 2]
                #Diff = math.sqrt((b1 - Red[0]) * (b1 - Red[0]) +
                                 #(g1 - Red[1]) * (g1 - Red[1]) +
                                 #(r1 - Red[2]) * (r1 - Red[2]))
                #if (Diff < threshold):
                    #print("red girdim")
                ravgX += x
                ravgY += y
                rcount += 1
        RcenterX = ravgX / rcount
        RcenterY = ravgY / rcount
        return RcenterX, RcenterY

    def findWhiteCenter(img):
        threshold = 60
        wavgX = 0
        wavgY = 0
        wcount = 0
        #White = [30, 0, 245]
        boundaries_white = [([0, 245, 245], [179, 255, 255])]

        for (lower,upper) in boundaries_white:
            low_boundary_white = np.array(lower,dtype="uint8")
            up_boundary_white = np.array(upper,dtype="uint8")
            mask_white = cv2.inRange(img,low_boundary_white,up_boundary_white)

        output = cv2.bitwise_and(img, img, mask=mask_white)
        cv2.imshow('final', output), cv2.waitKey(0), cv2.destroyAllWindows()
        white_arr = np.where(mask_white==255)
        print("white ",white_arr)

        for y in (white_arr[0]):
            for x in (white_arr[1]):
                #b1 = img[y, x, 0]
                #g1 = img[y, x, 1]
                #r1 = img[y, x, 2]
                #Diff = math.sqrt((b1 - White[0]) * (b1 - White[0]) +
                                 #(g1 - White[1]) * (g1 - White[1]) +
                                 #(r1 - White[2]) * (r1 - White[2]))
                #if (Diff < threshold):
                    #print("white girdim")
                wavgX += x
                wavgY += y
                wcount += 1
        WcenterX = wavgX / wcount
        WcenterY = wavgY / wcount
        return WcenterX, WcenterY

    YcenterX, YcenterY = findYellowCenter(img)
    RcenterX, RcenterY = findRedCenter(img)
    WcenterX, WcenterY = findWhiteCenter(img)

    yCx = np.rint(YcenterX)
    yCy = np.rint(YcenterY)
    wCx = np.rint(WcenterX)
    wCy = np.rint(WcenterY)
    rCx = np.rint(RcenterX)
    rCy = np.rint(RcenterY)

    yCx = np.int16(yCx)
    yCy = np.int16(yCy)
    wCx = np.int16(wCx)
    wCy = np.int16(wCy)
    rCx = np.int16(rCx)
    rCy = np.int16(rCy)

    temp1 = np.int16(smallTemp / 2)
    temp2 = np.int16(bigTemp / 2)

    cropimgRs = frame[rCy - temp1:rCy + temp1, rCx - temp1:rCx + temp1]
    cropimgYs = frame[yCy - temp1:yCy + temp1, yCx - temp1:yCx + temp1]
    cropimgWs = frame[wCy - temp1:wCy + temp1, wCx - temp1:wCx + temp1]

    cropimgRb = frame[rCy - temp2:rCy + temp2, rCx - temp2:rCx + temp2]
    cropimgYb = frame[yCy - temp2:yCy + temp2, yCx - temp2:yCx + temp2]
    cropimgWb = frame[wCy - temp2:wCy + temp2, wCx - temp2:wCx + temp2]


    return cropimgRs, cropimgYs, cropimgWs, cropimgRb, cropimgYb, cropimgWb