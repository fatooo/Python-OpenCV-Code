import cv2
import numpy as np
import os
import glob
import time
import math
import matplotlib.pyplot as plt

start_time = time.time()

img_dir = "C:\\Users\\fatma\\Desktop\\Bilardo\\Pool_Table_Docs\\20fps"  # Enter Directory of all images
data_path = os.path.join(img_dir, '*g')
files = glob.glob(data_path)
data = []
initial_window = 200
fps = 20 #frames per second
ppm = 370 #pixel per meter
w = initial_window
template_o = cv2.imread('white_big.png')
template_2_o = cv2.imread('white_ball_sym.png')
#template = cv2.GaussianBlur(template,(9,9),-1)
template = np.float32(template_o)
template_2= np.float32(template_2_o)
template_x = template.shape[0]
template_y = template.shape[1]
#print(template_x,template_y)
template_x_2 = template_2.shape[0]
template_y_2 = template_2.shape[1]
#print(template_x_2,template_y_2)

frame_amount = 152  #152 for 20fps & 39 for 5 fps & 43 for 5fps new & 225 for 30fps

method = cv2.TM_SQDIFF  #method used to check the correlation between the template and the frame

for f1 in files:
    img = cv2.imread(f1)
    data.append(img)

min_val = [0] * frame_amount
max_val = [0] * frame_amount
min_loc = [[0] * 2 for i in range(frame_amount)]
max_loc = [[0] * 2 for i in range(frame_amount)]

min_val_2 = [0] * frame_amount
max_val_2 = [0] * frame_amount
min_loc_2 = [[0] * 2 for i in range(frame_amount)]
max_loc_2 = [[0] * 2 for i in range(frame_amount)]

x_prime = [0] * frame_amount
y_prime = [0] * frame_amount

velocity = [0] * (frame_amount)
velocity_x = [0] * frame_amount
velocity_y = [0] * frame_amount

for i in range(frame_amount):
    half_window = w/2
    if i - 1 == -1:
        img_crop = data[0]
    else:
        if y_prime[i - 1] - half_window < 0:
            y_start = 0
        else:
            y_start = y_prime[i - 1] - half_window
        if x_prime[i - 1] - half_window < 0:
            x_start = 0
        else:
            x_start = x_prime[i - 1] - half_window

        if y_prime[i - 1] + half_window > img.shape[1]:
            y_stop = img.shape[0]
        else:
            y_stop = y_start + w
        if x_prime[i - 1] + half_window > img.shape[0]:
            x_stop = img.shape[1]
        else:
            x_stop = x_start + w
        # print(x_start,x_stop,y_start,y_stop)
        img_crop = data[i][int(x_start):int(x_stop), int(y_start):int(y_stop)]
        #cv2.imshow('crop',img_crop),cv2.waitKey(0), cv2.destroyAllWindows()

    img_crop = np.float32(img_crop)
    res = cv2.matchTemplate(img_crop, template, method)
    min_val[i], max_val[i], min_loc[i], max_loc[i] = cv2.minMaxLoc(res)

    est_x = int(min_loc[i][1] + velocity_x[i-1] * (1 / fps))
    est_y = int(min_loc[i][0] + velocity_y[i-1] * (1 / fps))

    # print("found ball",min_loc[i])
    if i == 0:
        x_prime[i] = est_x + 11 #why 11 & 17?

        y_prime[i] = est_y + 17
    else:
        if x_prime[i - 1] - half_window < 0:
            x_prime[i] = x_prime[i - 1] - half_window + est_x + (half_window - x_prime[i - 1])
        else:
            x_prime[i] = x_prime[i - 1] - half_window + est_x
        if y_prime[i - 1] - half_window < 0:
            y_prime[i] = y_prime[i - 1] - half_window + est_y + (half_window - y_prime[i - 1])
        else:
            y_prime[i] = y_prime[i - 1] - half_window + est_y

        #print("1",y_prime[i], x_prime[i])
        template_o = data[i][int(x_prime[i]):int(x_prime[i])+template_x, int(y_prime[i]):int(y_prime[i])+template_y] #update the template with the ball found in the current frame
        template_o = cv2.GaussianBlur(template_o, (5, 5), -1)
        #print(template_x, template_y)
        #cv2.imshow('final', template_o), cv2.waitKey(0), cv2.destroyAllWindows() #run to see the template used for the search in the next frame
        template = np.float32(template_o)
        res_2 = cv2.matchTemplate(template, template_2, method)
        min_val_2[i], max_val_2[i], min_loc_2[i], max_loc_2[i] = cv2.minMaxLoc(res_2)
        #print(min_loc_2[i][1],min_loc_2[i][0])
        cv2.circle(template_o, (int(min_loc_2[i][0]+1) + int(template_y_2 / 2), int(min_loc_2[i][1]) + int(template_x_2 / 2)), 2,
                   (0, 0, 255), -1)
        rect = cv2.rectangle(template_o, (int(min_loc_2[i][0]+2), int(min_loc_2[i][1])),
                             (int(min_loc_2[i][0] + template_y_2), int(min_loc_2[i][1] + template_x_2)), (0, 255, 0), 1)
        #cv2.imshow('final', template_o), cv2.waitKey(0), cv2.destroyAllWindows()
        x_prime[i] = x_prime[i] + template_x / 2 - template_x_2 / 2 + min_loc_2[i][1]
        y_prime[i] = y_prime[i] + template_y / 2 - template_y_2 / 2 + min_loc_2[i][0]
        #print("2",y_prime[i], x_prime[i])
        #print("--------------")

    # print("--------------")
    velocity_x[i] = abs(x_prime[i] - x_prime[i - 1])/fps
    velocity_y[i] = abs(y_prime[i] - y_prime[i - 1])/fps

    #print(velocity_x[i],velocity_x[i])
    #print(w)
#velocity[0] = 0
#plt.plot(velocity),plt.ylabel('Velocity (m/s)'),plt.xlabel('Frame'),plt.show()

for i in range(frame_amount):
    if i - 1 == -1:
        i = i + 1
    #print(y_prime[i-1],x_prime[i-1])
    cv2.line(data[frame_amount-1], (int(y_prime[i-1]-(int(template_y/2)-int(template_y_2/2))+int(template_y_2/2)), int(x_prime[i-1]-(int(template_x/2)-int(template_x_2/2))+template_x_2/2)), (int(y_prime[i]-(int(template_y/2)-int(template_y_2/2))+int(template_y_2/2)), int(x_prime[i]-(int(template_x/2)-int(template_x_2/2))+template_x_2/2)), (255, 255, 255), 1)
    cv2.circle(data[frame_amount-1],  (int(y_prime[i]-(int(template_y/2)-int(template_y_2/2))+int(template_y_2/2)),int(x_prime[i]-(int(template_x/2)-int(template_x_2/2))+template_x_2/2)), 2, (0, 0, 255), -1)
    #rect = cv2.rectangle(data[i], (int(y_prime[i]-(int(template_y/2)-int(template_y_2/2))),int(x_prime[i]-(int(template_x/2)-int(template_x_2/2)))), (int(y_prime[i]-(int(template_y/2)-int(template_y_2/2))+template_y_2),int(x_prime[i]-(int(template_x/2)-int(template_x_2/2))+template_x_2)), (0, 255, 0),1)
    #cv2.imshow('final', data[i]), cv2.waitKey(0), cv2.destroyAllWindows()

print("--- %s seconds ---" % (time.time() - start_time))

cv2.imshow('final', data[frame_amount-1]), cv2.waitKey(0),cv2.destroyAllWindows()