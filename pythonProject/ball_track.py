import cv2
import numpy as np
import os
import glob
import time

start_time = time.time()

img_dir = "C:\\Users\\fatma\\Desktop\\Bilardo\\Pool_Table_Docs\\5fps"  # Enter Directory of all images
data_path = os.path.join(img_dir, '*g')
files = glob.glob(data_path)
data = []
data_gray = []
template = cv2.imread('white_ball.png')
#gray_template = cv2.cvtColor(template,cv2.COLOR_BGR2GRAY)
gray_template = template
gray_template = np.float32(gray_template)
frame_amount = 39 #152 for 20fps & 39 for 5 fps & 43 for 5fps new

method = cv2.TM_SQDIFF #method used to check the correlation between the template and the frame

for f1 in files:
    img = cv2.imread(f1)
    data.append(img)


min_val = [0]*frame_amount
max_val = [0]*frame_amount
min_loc = [ [0]*2 for i in range(frame_amount)]
max_loc = [ [0]*2 for i in range(frame_amount)]

for i in range(frame_amount):
    #blur = cv2.GaussianBlur(data[i],(9,9),-1)
    #gray_img = cv2.cvtColor(blur, cv2.COLOR_BGR2GRAY)
    #gray_data = cv2.cvtColor(data[i], cv2.COLOR_BGR2GRAY)

    gray_img_crop = np.float32(data[i])
    res = cv2.matchTemplate(gray_img_crop, gray_template, method)
    min_val[i], max_val[i], min_loc[i], max_loc[i] = cv2.minMaxLoc(res)
    print((min_loc[i]))

for i in range(frame_amount):
    if i - 1 == -1:
        i = i + 1
    #rect = cv2.rectangle(data[i], (min_loc[i][0], min_loc[i][1]), (min_loc[i][0] + 30, min_loc[i][1] + 30), (0, 255, 0), 3)
    #cv2.imshow('rect', rect)
    #cv2.waitKey(0)
    #cv2.destroyAllWindows()
    cv2.line(data[frame_amount-1], (min_loc[i-1][0]+15, min_loc[i-1][1]+15), (min_loc[i][0]+15, min_loc[i][1]+15), (255, 255, 255), 1)
print("--- %s seconds ---" % (time.time() - start_time))
cv2.imshow('final', data[frame_amount-1])
cv2.waitKey(0)
cv2.destroyAllWindows()