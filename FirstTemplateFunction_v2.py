import cv2
import numpy as np
from numba import njit
import math
import time

start = time.time()

def ip(img, trasab, corners, vectors, N):  # N 100
    for y in range(vectors.shape[0]):
        for x in range(vectors.shape[1]):
            trasab[y00 + (N * y), x00 + (N * x)] = img[np.int16(corners[y, x, 1]), np.int16(corners[y, x, 0])]
            vectors[y, x, 0] = (np.int16(corners[y, x, 0]) - (x00 + N * x))  # x
            vectors[y, x, 1] = (np.int16(corners[y, x, 1]) - (y00 + N * y))  # y
    return vectors


def bugra(img, t_rasa_b, vectors):
    for y in range(img.shape[0] - 1):
        for x in range(img.shape[1] - 1):
            coefx = ((x - x00) / 100)
            rcoefx = np.int(coefx)
            coefy = ((y - y00) / 100)
            rcoefy = np.int(coefy)
            if ((coefx >= 0) & (coefy >= 0) & (coefx <= vectors.shape[1] - 1) & (coefy <= vectors.shape[0] - 1)):
                v00 = vectors[rcoefy, rcoefx]
                v10 = vectors[rcoefy + 1, rcoefx]
                v01 = vectors[rcoefy, rcoefx + 1]
                v11 = vectors[rcoefy + 1, rcoefx + 1]

                Dx = x - (x00 + rcoefx * 100)
                Dy = y - (y00 + rcoefy * 100)

                x_map = (((v00[0] * (100 - Dx) * (100 - Dy))
                          + (v10[0] * (100 - Dx) * (Dy))
                          + (v01[0] * Dx * (100 - Dy))
                          + (v11[0] * Dx * Dy))
                         / 10000)
                y_map = (((v00[1] * (100 - Dx) * (100 - Dy))
                          + (v10[1] * (100 - Dx) * (Dy))
                          + (v01[1] * Dx * (100 - Dy))
                          + (v11[1] * Dx * Dy))
                         / 10000)
                t_rasa_b[y, x] = img[y + np.int16(np.rint(y_map)),
                                     x + np.int16(np.rint(x_map))]
            else:
                t_rasa_b[y, x] = 0
    return t_rasa_b


def firstTemp(frame,blurTrasa, smallTemp, bigTemp):
    def findYellowCenter(img):
        threshold = 5
        yavgX = 0
        yavgY = 0
        ycount = 0
        Yellow = [30,227,255]#[0, 255, 255]

        for y in range(img.shape[0]):
            for x in range(img.shape[1]):
                b1 = img[y, x, 0]
                g1 = img[y, x, 1]
                r1 = img[y, x, 2]
                Diff = math.sqrt((b1 - Yellow[0]) * (b1 - Yellow[0]) +
                                 (g1 - Yellow[1]) * (g1 - Yellow[1]) +
                                 (r1 - Yellow[2]) * (r1 - Yellow[2]))
                if (math.sqrt((b1 - Yellow[0]) * (b1 - Yellow[0])) < threshold) and (math.sqrt((g1 - Yellow[1]) * (g1 - Yellow[1])) < threshold) and (math.sqrt((r1 - Yellow[2]) * (r1 - Yellow[2])) < threshold):
                    yavgX += x
                    yavgY += y
                    ycount += 1
                    #print(x, y,b1,g1,r1)
                    #print('sari girdim')
        YcenterX = yavgX / ycount
        YcenterY = yavgY / ycount
        #print(YcenterX, YcenterY)
        return YcenterX, YcenterY

    def findRedCenter(img):
        threshold = 5
        ravgX = 0
        ravgY = 0
        rcount = 0
        Red = [14,255,255]#[30, 100, 255]
        for y in range(img.shape[0]):
            for x in range(img.shape[1]):
                b1 = img[y, x, 0]
                g1 = img[y, x, 1]
                r1 = img[y, x, 2]
                Diff = math.sqrt((b1 - Red[0]) * (b1 - Red[0]) +
                                 (g1 - Red[1]) * (g1 - Red[1]) +
                                 (r1 - Red[2]) * (r1 - Red[2]))
                if (math.sqrt((b1 - Red[0]) * (b1 - Red[0])) < threshold) and (math.sqrt((g1 - Red[1]) * (g1 - Red[1])) < threshold) and (math.sqrt((r1 - Red[2]) * (r1 - Red[2])) < threshold):
                    ravgX += x
                    ravgY += y
                    rcount += 1
                    #print(x, y,b1,g1,r1)
                    #print('kirmizi girdim')
        RcenterX = ravgX / rcount
        RcenterY = ravgY / rcount
        #print(RcenterX, RcenterY)
        return RcenterX, RcenterY

    def findWhiteCenter(img):
        threshold = 5
        wavgX = 0
        wavgY = 0
        wcount = 0
        White = [23, 4, 255]#[255,255,255]
        for y in range(img.shape[0]):
            for x in range(img.shape[1]):
                b1 = img[y, x, 0]
                g1 = img[y, x, 1]
                r1 = img[y, x, 2]
                Diff = math.sqrt((b1 - White[0]) * (b1 - White[0]) +
                                 (g1 - White[1]) * (g1 - White[1]) +
                                 (r1 - White[2]) * (r1 - White[2]))
                if (math.sqrt((b1 - White[0]) * (b1 - White[0])) < threshold) and (math.sqrt((g1 - White[1]) * (g1 - White[1])) < threshold) and (math.sqrt((r1 - White[2]) * (r1 - White[2])) < threshold):
                    wavgX += x
                    wavgY += y
                    wcount += 1
                    #print(x, y,b1,g1,r1)
                    #print('beyaz girdim')
        WcenterX = wavgX / wcount
        WcenterY = wavgY / wcount
        #print(WcenterX, WcenterY)
        return WcenterX, WcenterY

    RcenterX, RcenterY = findRedCenter(blurTrasa)
    YcenterX, YcenterY = findYellowCenter(blurTrasa)
    WcenterX, WcenterY = findWhiteCenter(blurTrasa)

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


