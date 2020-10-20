import cv2
import numpy as np
import os
import glob
import time
import math
import matplotlib.pyplot as plt

start_time = time.time()

img_dir = "C:\\Users\\fatma\\Desktop\\Bilardo\\Pool_Table_Docs\\30fps"  # Enter Directory of all images
data_path = os.path.join(img_dir, '*g')
files = glob.glob(data_path)
data = []
initial_window = 300
fps = 30 #frames per second
ppm = 370 #pixel per meter
w = initial_window
template = cv2.imread('white_big.png')
template = np.float32(template)
template_x = template.shape[0]
template_y = template.shape[1]
#print(template_x,template_y)
frame_amount = 225  #152 for 20fps & 39 for 5 fps & 43 for 5fps new & 225 for 30fps

method = cv2.TM_SQDIFF  #method used to check the correlation between the template and the frame

for f1 in files:
    img = cv2.imread(f1)
    data.append(img)
    #cv2.imshow('deneme', data[i]), cv2.waitKey(0), cv2.destroyAllWindows()

min_val = [0] * frame_amount
max_val = [0] * frame_amount
min_loc = [[0] * 2 for i in range(frame_amount)]
max_loc = [[0] * 2 for i in range(frame_amount)]
x_prime = [0] * frame_amount
y_prime = [0] * frame_amount

velocity = [0] * (frame_amount)

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
    img_crop = np.float32(img_crop)
    res = cv2.matchTemplate(img_crop, template, method)
    min_val[i], max_val[i], min_loc[i], max_loc[i] = cv2.minMaxLoc(res)
    # print("found ball",min_loc[i])
    if i == 0:
        x_prime[i] = min_loc[i][1]
        y_prime[i] = min_loc[i][0]
    else:
        if x_prime[i - 1] - half_window < 0:
            x_prime[i] = x_prime[i - 1] - half_window + min_loc[i][1] + (half_window - x_prime[i - 1])
        else:
            x_prime[i] = x_prime[i - 1] - half_window + min_loc[i][1]
        if y_prime[i - 1] - half_window < 0:
            y_prime[i] = y_prime[i - 1] - half_window + min_loc[i][0] + (half_window - y_prime[i - 1])
        else:
            y_prime[i] = y_prime[i - 1] - half_window + min_loc[i][0]

        #print(y_prime[i], x_prime[i])
        template = data[i][int(x_prime[i]):int(x_prime[i])+template_x, int(y_prime[i]):int(y_prime[i])+template_y] #update the template with the ball found in the current frame
        #cv2.imshow('final', template), cv2.waitKey(0), cv2.destroyAllWindows() #run to see the template used for the search in the next frame
        template = np.float32(template)

    # print("--------------")
    velocity[i] = math.sqrt(math.pow(x_prime[i] - x_prime[i - 1], 2) + math.pow(y_prime[i] - y_prime[i - 1], 2))*fps/ppm
    if velocity[i]>0.5 and velocity[i]<50:
        w = initial_window#int(velocity[i])*300
    elif velocity[i]>0 and velocity[i]<0.5:
        w = initial_window#int(velocity[i])*400
    else:
        w = initial_window
    #w=initial_window
    #print(velocity[i])
    #print(w)
#velocity[0] = 0
#plt.plot(velocity),plt.ylabel('Velocity (m/s)'),plt.xlabel('Frame'),plt.show()

for i in range(frame_amount):
    if i - 1 == -1:
        i = i + 1
    cv2.line(data[frame_amount-1], (int(y_prime[i-1]+int(template_y/2)+1), int(x_prime[i-1]+int(template_x/2)+1)), (int(y_prime[i]+int(template_y/2)+1), int(x_prime[i]+int(template_x/2)+1)), (255, 255, 255), 1)
    cv2.circle(data[frame_amount-1], (int(y_prime[i])+int(template_y/2)+1, int(x_prime[i])+int(template_x/2)+1), 2, (0, 0, 255), -1)
    rect = cv2.rectangle(data[i], (int(y_prime[i]), int(x_prime[i])), (int(y_prime[i]+template_y), int(x_prime[i]+template_x)), (0, 255, 0),1)
    #cv2.imshow('final', data[i]), cv2.waitKey(0), cv2.destroyAllWindows()

print("--- %s seconds ---" % (time.time() - start_time))

cv2.imshow('final', data[frame_amount-1]), cv2.waitKey(0),cv2.destroyAllWindows()
