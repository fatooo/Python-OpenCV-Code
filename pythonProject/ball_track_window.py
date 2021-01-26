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
big_templates = [] #array for the bigger template at each iteration
initial_window = 200 #size of the window in which we will look for the template
fps = 30 #frames per second
ppm_x = 550 #pixel per meter for x axis
ppm_y = 637 #pixel per meter for y axis
w = initial_window
template_o = cv2.imread('yellow_big_2.png') #bigger tenplate
template_2_o = cv2.imread('yellow_2.png') #smaller template
#template = cv2.GaussianBlur(template,(9,9),-1)
template = np.float32(template_o) #necessary for matchTemplate function use
template_2= np.float32(template_2_o) #necessary for matchTemplate function use
template_x = template.shape[0]
template_y = template.shape[1]

template_x_2 = template_2.shape[0]
template_y_2 = template_2.shape[1]

frame_amount = 420  #152 for 20fps & 39 for 5 fps & 43 for 5fps new & 225 for 30fps & 422 for salon data

method = cv2.TM_SQDIFF_NORMED  #method used to check the correlation between the template and the frame

cap = cv2.VideoCapture('video1.mp4')
fourcc = cv2.VideoWriter_fourcc(*'XVID')
out = cv2.VideoWriter('output.avi', fourcc, 20.0, (768,576))

data = [0] * frame_amount
# correlation values & indices for the first template search
min_val = [0] * frame_amount
max_val = [0] * frame_amount
min_loc = [[0] * 2 for k in range(frame_amount)]
max_loc = [[0] * 2 for k in range(frame_amount)]
# correlation values & indices for the second template search
min_val_2 = [0] * frame_amount
max_val_2 = [0] * frame_amount
min_loc_2 = [[0] * 2 for k in range(frame_amount)]
max_loc_2 = [[0] * 2 for k in range(frame_amount)]

x_prime = [0] * frame_amount
y_prime = [0] * frame_amount

velocity = [0] * (frame_amount)
velocity_x = [0] * frame_amount
velocity_y = [0] * frame_amount

# center of the current and previous detected template location for every iteration
center = [0]*frame_amount
center_prev = [0]*frame_amount

i = 0

while(i<frame_amount-1):
    ret, data[i] = cap.read()

    out.write(data[i])
    img_y = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
    img_x = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
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

        if y_prime[i - 1] + half_window > img_y:
            y_stop = img_y
        else:
            y_stop = y_start + w
        if x_prime[i - 1] + half_window >img_x:
            x_stop = img_x
        else:
            x_stop = x_start + w
        # crop the new window from the frame & we will do the search in this window
        img_crop = data[i][round(x_start):round(x_stop), round(y_start):round(y_stop)]
        #cv2.imshow('crop',img_crop),cv2.waitKey(0), cv2.destroyAllWindows()

    img_crop = np.float32(img_crop)
    res = cv2.matchTemplate(img_crop, template, method)
    #find the bigger template in the window within that frame
    min_val[i], max_val[i], min_loc[i], max_loc[i] = cv2.minMaxLoc(res)

    #estimated position of the ball in the next iteration
    est_x = round(min_loc[i][1])
    est_y = round(min_loc[i][0])

    #print("Estimated position: ",est_x,est_y)

    #Map the found location in this window to the bigger frame as in indices
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

        #update the template with the best match found in this iteration & in the next frame we will lok for this bigger template in the window
        template_o = data[i][round(x_prime[i]):round(x_prime[i])+template_x, round(y_prime[i]):round(y_prime[i])+template_y] #update the template with the ball found in the current frame
        #template_o = cv2.GaussianBlur(template_o, (5, 5), -1)

        #print(template_x, template_y)
        #add this new template into our array
    big_templates.append(template_o)

        #cv2.imshow('final', template_o), cv2.waitKey(0), cv2.destroyAllWindows() #run to see the template used for the search in the next frame

        #look for the smaller template in this bigger template
    template = np.float32(template_o)
    res_2 = cv2.matchTemplate(template, template_2, method)

    min_val_2[i], max_val_2[i], min_loc_2[i], max_loc_2[i] = cv2.minMaxLoc(res_2)

        ### USED FOR CIRLCE DETECTION INSTEAD OF THE SMALLER TEMPLATE (KEEP COMMENTED)
        #template_c = cv2.cvtColor(template_o, cv2.COLOR_BGR2GRAY)
        #template_c = cv2.medianBlur(template_c, 5)

        #circles = cv2.HoughCircles(template_c, cv2.HOUGH_GRADIENT, 1.5, 20,
                                   #param1=50, param2=30, minRadius=0, maxRadius=22)
        #circles = np.uint16(np.around(circles))
        #print(circles)
        #cv2.circle(template_o, (circles[0][0][0], circles[0][0][1]), circles[0][0][2], (0, 255, 0), 2)
        # draw the center of the circle
        #cv2.circle(template_o, (circles[0][0][0], circles[0][0][1]), 2, (0, 0, 255), 3)
        #cv2.imshow('circles', template_o), cv2.waitKey(0), cv2.destroyAllWindows()

        #min_loc_2[i] = (circles[0][0][0],circles[0][0][1])
        #print(min_loc_2[i][1],min_loc_2[i][0])
        #### END OF THE CODE USED FOR CIRCLE DETECTION INSTEAD OF SMALLER TEMPLATE

    cv2.circle(template_o, (round(min_loc_2[i][0]+1) + round(template_y_2 / 2), round(min_loc_2[i][1]) + round(template_x_2 / 2)), 2,
                   (0, 0, 255), -1)
        #rect = cv2.rectangle(template_o, (int(min_loc_2[i][0]+2), int(min_loc_2[i][1])),
                             #(int(min_loc_2[i][0] + template_y_2), int(min_loc_2[i][1] + template_x_2)), (0, 255, 0), 1)
    cv2.imshow('final', template_o), cv2.waitKey(0), cv2.destroyAllWindows() #visualize the updated bigger template

        #these are the coordinates of the point on where the correlation is the highest & corner point on the upper left
    x_prime[i] = x_prime[i] + template_x / 2 + min_loc_2[i][1] - template_x_2 / 2  #used for double template matching
    y_prime[i] = y_prime[i] + template_y / 2  + min_loc_2[i][0] - template_y_2 / 2

    center_prev[i] = (
    round(y_prime[i - 1] - (round(template_y / 2) - round(template_y_2 / 2)) + round(template_y_2 / 2)),
    round(x_prime[i - 1] - (round(template_x / 2) - round(template_x_2 / 2)) + template_x_2 / 2))
    center[i] = (round(y_prime[i] - (round(template_y / 2) - round(template_y_2 / 2)) + round(template_y_2 / 2)),
                 round(x_prime[i] - (round(template_x / 2) - round(template_x_2 / 2)) + template_x_2 / 2))
        #print("2",y_prime[i], x_prime[i])
        #print("--------------")
    center_prev[0] = center[0]
    #cv2.line(data[i], center_prev[i], center[i], (255, 255, 255), 1)
    cv2.circle(data[i], (center[i][0], center[i][1]), 2, (0, 0, 255), -1)

    imS = cv2.resize(data[i], (1200, 706))
    # cv2.imshow('final', imS)
    # if cv2.waitKey(1) & 0xFF == ord('q'):
    #     break
    i = i + 1
    print(i)
#velocity[0] = 0
cap.release(),out.release(),cv2.destroyAllWindows()
# for i in range(frame_amount):
#     if i - 1 == -1:
#         i = i + 1
#     #we need to add the half of the bigger template size to obtain the center
#
#     velocity_x[i] = abs(center[i][0] - center_prev[i][0]) * fps / ppm_x
#     velocity_y[i] = abs(center[i][1] - center_prev[i][1]) * fps / ppm_y
#     velocity[i] = math.sqrt(math.pow(velocity_x[i], 2) + math.pow(velocity_y[i], 2))
#     #print(velocity[i])
#
#     #center_prev = (int(y_prime[i-1]+(int(template_y/2))), int(x_prime[i-1]+(int(template_x/2))))
#     #center = (int(y_prime[i]+(int(template_y/2))), int(x_prime[i]+(int(template_x/2))))
#     cv2.line(data[i], center_prev[i] , center[i] , (255, 255, 255), 1)
#     cv2.circle(data[i],  (center[i][0],center[i][1]), 2, (0, 0, 255), -1)
#
#     #rect = cv2.rectangle(data[i], (int(y_prime[i]-(int(template_y/2)-int(template_y_2/2))),int(x_prime[i]-(int(template_x/2)-int(template_x_2/2)))), (int(y_prime[i]-(int(template_y/2)-int(template_y_2/2))+template_y_2),int(x_prime[i]-(int(template_x/2)-int(template_x_2/2))+template_x_2)), (0, 255, 0),1)
#     #cv2.rectangle(data[i],((center[0]-int(template_y/2)),center[1]-int(template_x/2)),((center[0]+int(template_y/2)),center[1]+int(template_x/2)), (0, 255, 0),2)
#     #cv2.rectangle(data[i], ((center[0] - int(template_y_2 / 2)), center[1] - int(template_x_2 / 2)),
#                          #((center[0] + int(template_y_2 / 2)), center[1] + int(template_x_2 / 2)), (0, 255, 0), 2)
#     #font = cv2.FONT_HERSHEY_SIMPLEX
#     imS = cv2.resize(data[i], (1200, 706))
#     #cv2.putText(imS, str(velocity[i]), (700, 500), font, 1, (255, 255, 255), 2, cv2.LINE_AA)
#     cv2.imshow('final', imS), cv2.waitKey(0), cv2.destroyAllWindows()

#plt.plot(velocity),plt.ylabel('Velocity (m/s)'),plt.xlabel('Frame'),plt.show()
#print("--- %s seconds ---" % (time.time() - start_time)) # overall process time
np.savetxt("white_center_1.csv",center,delimiter=",",fmt='%s')
# imS = cv2.resize(data[frame_amount-1], (960, 540))
# cv2.imshow('final', imS), cv2.waitKey(0),cv2.destroyAllWindows()
#print(center)
#min_val_fin = max(min_val)
#print("Min value final : ",min_val_fin)

#write the processed frames into a folder

# path = 'C:\\Users\\fatma\\Desktop\\Bilardo\\Pool_Table_Docs\\processed_data1'

# for i in range(frame_amount-4):
#     i = i + 3
#     for k in range(i-2):
#         k = k + 2
#         cv2.line(data[i], center_prev[k], center[k], (255, 255, 255), 2)
#         cv2.circle(data[i], (center_prev[k][0],center_prev[k][1]), 2, (0, 0, 255), -1)
#     imS = cv2.resize(data[i], (960, 540))
#     font = cv2.FONT_HERSHEY_SIMPLEX
#     cv2.putText(imS,str(round(velocity[i],2)), (700, 500), font, 1, (255, 255, 255), 2, cv2.LINE_AA)
#     print("i ",i,center[i])
#     cv2.imshow('final', imS), cv2.waitKey(0), cv2.destroyAllWindows()
#     if i<10:
#         cv2.imwrite(os.path.join(path, 'img_00%d.jpg' % i), imS)
#     elif i>=10 and i<100:
#          cv2.imwrite(os.path.join(path, 'img_0%d.jpg' % i), imS)
#     else:
#          cv2.imwrite(os.path.join(path, 'img_%d.jpg' % i), imS)
