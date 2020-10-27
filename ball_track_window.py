import cv2
import numpy as np
import os
import glob
import time
import math
import matplotlib.pyplot as plt

start_time = time.time()

img_dir = "C:\\Users\\fatma\\Desktop\\Bilardo\\Pool_Table_Docs\\video_data2"  # Enter Directory of all images
data_path = os.path.join(img_dir, '*g')
files = glob.glob(data_path)
data = []
big_templates = []
initial_window = 200
fps = 30 #frames per second
ppm = 370 #pixel per meter
w = initial_window
template_o = cv2.imread('salon_white_big.png')
template_2_o = cv2.imread('white_salon.png')
#template = cv2.GaussianBlur(template,(9,9),-1)
template = np.float32(template_o)
template_2= np.float32(template_2_o)
template_x = template.shape[0]
template_y = template.shape[1]
#print(template_x,template_y)
template_x_2 = template_2.shape[0]
template_y_2 = template_2.shape[1]
#template_x_2 = 0
#template_y_2 = 0
#print(template_x_2,template_y_2)

frame_amount = 422  #152 for 20fps & 39 for 5 fps & 43 for 5fps new & 225 for 30fps & 422 for salon data

method = cv2.TM_SQDIFF_NORMED  #method used to check the correlation between the template and the frame

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

center = [0]*frame_amount
center_prev = [0]*frame_amount

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
        img_crop = data[i][int(x_start):int(x_stop), int(y_start):int(y_stop)]
        #cv2.imshow('crop',img_crop),cv2.waitKey(0), cv2.destroyAllWindows()

    img_crop = np.float32(img_crop)
    res = cv2.matchTemplate(img_crop, template, method)
    min_val[i], max_val[i], min_loc[i], max_loc[i] = cv2.minMaxLoc(res)

    est_x = int(min_loc[i][1] + velocity_x[i-1] * (1 / fps))
    est_y = int(min_loc[i][0] + velocity_y[i-1] * (1 / fps))

    #print("Estimated position: ",est_x,est_y)
    if i == 0:
        x_prime[i] = est_x  #why 11 & 17?

        y_prime[i] = est_y
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
        #template_o = cv2.GaussianBlur(template_o, (5, 5), -1)

        #print(template_x, template_y)
        big_templates.append(template_o)

        #cv2.imshow('final', template_o), cv2.waitKey(0), cv2.destroyAllWindows() #run to see the template used for the search in the next frame

        template = np.float32(template_o)
        #res_2 = cv2.matchTemplate(template, template_2, method)

        #min_val_2[i], max_val_2[i], min_loc_2[i], max_loc_2[i] = cv2.minMaxLoc(res_2)

        template_c = cv2.cvtColor(template_o, cv2.COLOR_BGR2GRAY)
        template_c = cv2.medianBlur(template_c, 5)

        circles = cv2.HoughCircles(template_c, cv2.HOUGH_GRADIENT, 1.5, 20,
                                   param1=50, param2=30, minRadius=0, maxRadius=0)
        circles = np.uint16(np.around(circles))
        #print(circles)
        #cv2.circle(template_o, (circles[0][0][0], circles[0][0][1]), circles[0][0][2], (0, 255, 0), 2)
        # draw the center of the circle
        cv2.circle(template_o, (circles[0][0][0], circles[0][0][1]), 2, (0, 0, 255), 3)
        #cv2.imshow('circles', template_o), cv2.waitKey(0), cv2.destroyAllWindows()

        min_loc_2[i] = (circles[0][0][0],circles[0][0][1])
        #print(min_loc_2[i][1],min_loc_2[i][0])

        #cv2.circle(template_o, (int(min_loc_2[i][0]+1) + int(template_y_2 / 2), int(min_loc_2[i][1]) + int(template_x_2 / 2)), 2,
                   #(0, 0, 255), -1)
        #rect = cv2.rectangle(template_o, (int(min_loc_2[i][0]+2), int(min_loc_2[i][1])),
                             #(int(min_loc_2[i][0] + template_y_2), int(min_loc_2[i][1] + template_x_2)), (0, 255, 0), 1)
        #cv2.imshow('final', template_o), cv2.waitKey(0), cv2.destroyAllWindows()


        x_prime[i] = x_prime[i] - template_x / 2 + min_loc_2[i][1] #used for double template matching - template_x_2 / 2
        y_prime[i] = y_prime[i] - template_y / 2  + min_loc_2[i][0] #- template_y_2 / 2

        #print("2",y_prime[i], x_prime[i])
        #print("--------------")

    # print("--------------")

#velocity[0] = 0

for i in range(frame_amount):
    if i - 1 == -1:
        i = i + 1

    center_prev[i] = (int(y_prime[i-1]-(int(template_y/2)-int(template_y_2/2))+int(template_y_2/2)), int(x_prime[i-1]-(int(template_x/2)-int(template_x_2/2))+template_x_2/2))
    center[i] = (int(y_prime[i]-(int(template_y/2)-int(template_y_2/2))+int(template_y_2/2)), int(x_prime[i]-(int(template_x/2)-int(template_x_2/2))+template_x_2/2))

    velocity_x[i] = abs(center[i][0] - center_prev[i][0]) / fps
    velocity_y[i] = abs(center[i][1] - center_prev[i][1]) / fps
    velocity[i] = math.sqrt(math.pow(velocity_x[i], 2) + math.pow(velocity_y[i], 2))
    print(velocity[i])

    #center_prev = (int(y_prime[i-1]+(int(template_y/2))), int(x_prime[i-1]+(int(template_x/2))))
    #center = (int(y_prime[i]+(int(template_y/2))), int(x_prime[i]+(int(template_x/2))))
    cv2.line(data[frame_amount-1], center_prev[i] , center[i] , (255, 255, 255), 1)
    cv2.circle(data[frame_amount-1],  (center[i][0],center[i][1]), 2, (0, 0, 255), -1)

    #rect = cv2.rectangle(data[i], (int(y_prime[i]-(int(template_y/2)-int(template_y_2/2))),int(x_prime[i]-(int(template_x/2)-int(template_x_2/2)))), (int(y_prime[i]-(int(template_y/2)-int(template_y_2/2))+template_y_2),int(x_prime[i]-(int(template_x/2)-int(template_x_2/2))+template_x_2)), (0, 255, 0),1)
    #cv2.rectangle(data[i],((center[0]-int(template_y/2)),center[1]-int(template_x/2)),((center[0]+int(template_y/2)),center[1]+int(template_x/2)), (0, 255, 0),2)
    #cv2.rectangle(data[i], ((center[0] - int(template_y_2 / 2)), center[1] - int(template_x_2 / 2)),
                         #((center[0] + int(template_y_2 / 2)), center[1] + int(template_x_2 / 2)), (0, 255, 0), 2)

    imS = cv2.resize(data[i], (1200, 706))
    cv2.imshow('final', imS), cv2.waitKey(0), cv2.destroyAllWindows()

#plt.plot(velocity),plt.ylabel('Velocity (m/s)'),plt.xlabel('Frame'),plt.show()
print("--- %s seconds ---" % (time.time() - start_time))
imS = cv2.resize(data[frame_amount-1], (960, 540))
cv2.imshow('final', imS), cv2.waitKey(0),cv2.destroyAllWindows()


path = 'C:\\Users\\fatma\\Desktop\\Bilardo\\Pool_Table_Docs\\processed_data'

# for i in range(frame_amount-4):
#     i = i + 3
#     for k in range(i-2):
#         k = k + 2
#         cv2.line(data[i], center_prev[k], center[k], (255, 255, 255), 2)
#     imS = cv2.resize(data[i], (960, 540))
#     font = cv2.FONT_HERSHEY_SIMPLEX
#     cv2.putText(imS,str(velocity[i]), (700, 500), font, 1, (255, 255, 255), 2, cv2.LINE_AA)
#     #print("i ",i,center[i])
#     cv2.imshow('final', imS), cv2.waitKey(0), cv2.destroyAllWindows()
#     if i<10:
#         cv2.imwrite(os.path.join(path, 'img_00%d.jpg' % i), imS)
#     elif i>=10 and i<100:
#         cv2.imwrite(os.path.join(path, 'img_0%d.jpg' % i), imS)
#     else:
#         cv2.imwrite(os.path.join(path, 'img_%d.jpg' % i), imS)
