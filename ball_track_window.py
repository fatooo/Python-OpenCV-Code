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
w = 300
template = cv2.imread('white_ball.png')
template = np.float32(template)
frame_amount = 39  #152 for 20fps & 39 for 5 fps & 43 for 5fps new

method = cv2.TM_SQDIFF  #method used to check the correlation between the template and the frame

for f1 in files:
    img = cv2.imread(f1)
    data.append(img)

min_val = [0] * frame_amount
max_val = [0] * frame_amount
min_loc = [[0] * 2 for i in range(frame_amount)]
max_loc = [[0] * 2 for i in range(frame_amount)]
x_prime = [0] * frame_amount
y_prime = [0] * frame_amount

for i in range(frame_amount):
    if i - 1 == -1:
        img_crop = data[0]
    else:
        if y_prime[i - 1] - (w / 2) < 0:
            y_start = 0
        else:
            y_start = y_prime[i - 1] - (w / 2)
        if x_prime[i - 1] - (w / 2) < 0:
            x_start = 0
        else:
            x_start = x_prime[i - 1] - (w / 2)

        if y_prime[i - 1] + (w / 2) > img.shape[1]:
            y_stop = img.shape[0]
        else:
            y_stop = y_start + w
        if x_prime[i - 1] + (w / 2) > img.shape[0]:
            x_stop = img.shape[1]
        else:
            x_stop = x_start + w
        # print(x_start,x_stop,y_start,y_stop)
        img_crop = data[i][int(x_start):int(x_stop), int(y_start):int(y_stop)]
    # cv2.imshow('final', img_crop),cv2.waitKey(0),cv2.destroyAllWindows()
    img_crop = np.float32(img_crop)
    res = cv2.matchTemplate(img_crop, template, method)
    min_val[i], max_val[i], min_loc[i], max_loc[i] = cv2.minMaxLoc(res)
    # print("found ball",min_loc[i])
    if i == 0:
        x_prime[i] = min_loc[i][1]
        y_prime[i] = min_loc[i][0]
    else:
        if x_prime[i - 1] - (w / 2) < 0:
            x_prime[i] = x_prime[i - 1] - (w / 2) + min_loc[i][1] + ((w / 2) - x_prime[i - 1])
        else:
            x_prime[i] = x_prime[i - 1] - (w / 2) + min_loc[i][1]
        if y_prime[i - 1] - (w / 2) < 0:
            y_prime[i] = y_prime[i - 1] - (w / 2) + min_loc[i][0] + ((w / 2) - y_prime[i - 1])
        else:
            y_prime[i] = y_prime[i - 1] - (w / 2) + min_loc[i][0]
    # print(y_prime[i],x_prime[i])
    # print("--------------")

for i in range(frame_amount):
    if i - 1 == -1:
        i = i + 1
    cv2.line(data[frame_amount-1], (int(y_prime[i-1]+15), int(x_prime[i-1]+15)), (int(y_prime[i]+15), int(x_prime[i]+15)), (255, 255, 255), 1)
print("--- %s seconds ---" % (time.time() - start_time))
cv2.imshow('final', data[frame_amount-1])
cv2.waitKey(0)
cv2.destroyAllWindows()
