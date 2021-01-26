from ball_track_window_white import white_track
from ball_track_window_yellow import yellow_track
from ball_track_window_red import red_track
from fish_eye_correct import fish_eye_correct
from demo import demo
import cv2
import numpy as np
from numba import njit
import time
from datetime import datetime
from movefunction import Move
from movefunction import NoMove
from sideTouch import side_touch
#from firstTemplate import firstTemp
from FirstTemplateFunction_v2 import firstTemp
dateTimeObj = datetime.now()
dateObj = dateTimeObj.date()
timeObj = dateTimeObj.time()
timeStr = timeObj.strftime("%H%M%S_")
dateStr = dateObj.strftime("%b%d%Y_")

#import the big templates for each ball
#template_w = cv2.imread('C:\\Users\\fatma\\PycharmProjects\\pythonProject\\Templates\\deneme_white.png')
#template_y = cv2.imread('C:\\Users\\fatma\\PycharmProjects\\pythonProject\\Templates\\yellow_big_2.png')
#template_r = cv2.imread('C:\\Users\\fatma\\PycharmProjects\\pythonProject\\Templates\\red_zor_big.png')
#template_2_w = cv2.imread('C:\\Users\\fatma\\PycharmProjects\\pythonProject\\Templates\\white_2.png')
#template_2_y = cv2.imread('C:\\Users\\fatma\\PycharmProjects\\pythonProject\\Templates\\yellow_2.png')
#template_2_r = cv2.imread('C:\\Users\\fatma\\PycharmProjects\\pythonProject\\Templates\\red_2.png')

#template_w = cv2.cvtColor(template_w, cv2.COLOR_BGR2HSV)
#template_y = cv2.cvtColor(template_y, cv2.COLOR_BGR2HSV)
#template_r = cv2.cvtColor(template_r, cv2.COLOR_BGR2HSV)
#template_2_w = cv2.cvtColor(template_2_w, cv2.COLOR_BGR2HSV)
#template_2_y = cv2.cvtColor(template_2_y, cv2.COLOR_BGR2HSV)
#template_2_r = cv2.cvtColor(template_2_r, cv2.COLOR_BGR2HSV)

#v2.imshow("cropimg3", template_2_r), cv2.waitKey(0), cv2.destroyAllWindows()
#cv2.imshow("cropimg3", template_2_y), cv2.waitKey(0), cv2.destroyAllWindows()
#cv2.imshow("cropimg3", template_2_w), cv2.waitKey(0), cv2.destroyAllWindows()
#cv2.imshow("cropimg3", template_r), cv2.waitKey(0), cv2.destroyAllWindows()
#cv2.imshow("cropimg3", template_y), cv2.waitKey(0), cv2.destroyAllWindows()
#cv2.imshow("cropimg3", template_w), cv2.waitKey(0), cv2.destroyAllWindows()
#open the webcam

cap = cv2.VideoCapture('C:\\Users\\fatma\\PycharmProjects\\pythonProject\\video4.mp4')
#fourcc = cv2.VideoWriter_fourcc(*'DVIX')
#out = cv2.VideoWriter('C:\\Users\\fatma\\PycharmProjects\\pythonProject\\Outputs\\'+str(dateStr)+str(timeStr)+'output.mp4v',cv2.VideoWriter_fourcc(*'XVID'),60, (1920, 1080))

#cap = cv2.VideoCapture(1)
#if not (cap.isOpened()):
    #print("Could not open video device")
#set webcam frame resolution
#cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
#cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)

data = [] #the frames will be appended into this array
data_w = [] #white ball position data array
data_y = [] #yellow ball position data array
data_r = [] #red ball position data array
# white ball matched template corner arrays
x_prime_w = []
y_prime_w = []
# yellow ball matched template corner arrays
x_prime_y = []
y_prime_y = []
# red ball matched template corner arrays
x_prime_r = []
y_prime_r = []
# white ball velocity vectors
velocity_x_w = []
velocity_y_w = []
# yellow ball velocity vectors
velocity_x_y = []
velocity_y_y = []
# red ball velocity vectors
velocity_x_r = []
velocity_y_r = []
# Velocity value arrays for every ball
velocity_w = []
velocity_y = []
velocity_r = []
# cropped image start & stop pixels for every ball (initialized to 0 sent to eavh track function as input and returned again at the end of the function)
x_start_r = 0 ; y_start_r = 0 ; x_stop_r = 0 ; y_stop_r = 0
x_start_y = 0 ; y_start_y = 0 ; x_stop_y = 0 ; y_stop_y = 0
x_start_w = 0 ; y_start_w = 0 ; x_stop_w = 0 ; y_stop_w = 0

first_move = [1,1,1]

i = 0
max_vel_y = 0
max_vel_w = 0
max_vel_r = 0

map_x = np.loadtxt('map_x_idx.csv', delimiter=',')
map_y = np.loadtxt('map_y_idx.csv', delimiter=',')

coords = np.ndarray(shape=(1080 * 1920, 2), dtype=int)
coords_T = np.zeros(shape=(2,1080*1920),dtype=int)
for m in range(140,940):
    for k in range(160,1760):
        coords[m*1920+k][:]=int(map_y[m][k]),int(map_x[m][k])
coords_T = coords.T
coords_T_list = coords_T.tolist()
print(type(coords_T_list))
NoMotion_flag = True
delete_flag = False

while(True):
    start_time = time.time()
    ret, frame = cap.read()

    #start_time = time.time()
    #c_std = njit(fish_eye_correct)
    frame = fish_eye_correct(frame, coords_T)

    #cv2.imshow("cropimg3", frame), cv2.waitKey(0), cv2.destroyAllWindows()
    #print(i , "--- %s seconds ---" % (time.time() - start_time))
    # out.write(frame)
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    if i == 0:
        #blurTrasa = cv2.GaussianBlur(frame, (41, 41), -1)
        touch = []
        points = []
        side_touch_w = False
        side_touch_y = False
        side_touch_r = False

        c_std = njit(firstTemp)
        template_2_r,template_2_y,template_2_w,template_r,template_y,template_w = c_std(frame,frame,38,90)
        #template_2_r = cv2.cvtColor(template_2_r, cv2.COLOR_BGR2HSV)
        #template_2_y = cv2.cvtColor(template_2_y, cv2.COLOR_BGR2HSV)
        #template_2_w = cv2.cvtColor(template_2_w, cv2.COLOR_BGR2HSV)
        #template_r = cv2.cvtColor(template_r, cv2.COLOR_BGR2HSV)
        #template_y = cv2.cvtColor(template_y, cv2.COLOR_BGR2HSV)
        #template_w = cv2.cvtColor(template_w, cv2.COLOR_BGR2HSV)
        #cv2.imshow("cropimg3", template_2_r), cv2.waitKey(0), cv2.destroyAllWindows()
        #cv2.imshow("cropimg3", template_2_y), cv2.waitKey(0), cv2.destroyAllWindows()
        #cv2.imshow("cropimg3", template_2_w), cv2.waitKey(0), cv2.destroyAllWindows()
        #cv2.imshow("cropimg3", template_r), cv2.waitKey(0), cv2.destroyAllWindows()
        #cv2.imshow("cropimg3", template_y), cv2.waitKey(0), cv2.destroyAllWindows()
        #cv2.imshow("cropimg3", template_w), cv2.waitKey(0), cv2.destroyAllWindows()

    data.append(frame)

    template_w,velocity_x_w,velocity_y_w,velocity_w,data,data_w,x_start_w,y_start_w,x_stop_w,y_stop_w,center_prev_w,center_w = white_track(side_touch_w,frame,i,data,data_w,template_w,template_2_w,x_prime_w,y_prime_w,velocity_x_w,velocity_y_w,velocity_w,x_start_w,y_start_w,x_stop_w,y_stop_w)
    template_y,velocity_x_y,velocity_y_y,velocity_y,data,data_y,x_start_y,y_start_y,x_stop_y,y_stop_y,center_prev_y,center_y = yellow_track(side_touch_y,frame,i,data,data_y,template_y,template_2_y,x_prime_y,y_prime_y,velocity_x_y,velocity_y_y,velocity_y,x_start_y,y_start_y,x_stop_y,y_stop_y)
    template_r,velocity_x_r,velocity_y_r,velocity_r,data,data_r,x_start_r,y_start_r,x_stop_r,y_stop_r,center_prev_r,center_r = red_track(side_touch_r,frame,i,data,data_r,template_r,template_2_r,x_prime_r,y_prime_r,velocity_x_r,velocity_y_r,velocity_r,x_start_r,y_start_r,x_stop_r,y_stop_r)
    side_touch_w,side_touch_y,side_touch_r,touch = side_touch(center_w,velocity_x_w,velocity_y_w,center_y,velocity_x_y,velocity_y_y,center_r,velocity_x_r,velocity_y_r,i,touch,points)

    if NoMotion_flag:
        white_motion = NoMove(center_prev_w[1],center_prev_w[0],center_w[1],center_w[0]) #returns True if no motion detected & False otherwise
        yellow_motion = NoMove(center_prev_y[1],center_prev_y[0],center_y[1],center_y[0])
        red_motion = NoMove(center_prev_r[1],center_prev_r[0],center_r[1],center_r[0])
        NoMotion_flag = white_motion and yellow_motion and red_motion

    if (NoMotion_flag==True) or ((Move(center_prev_w[1],center_prev_w[0],center_w[1],center_w[0]) and Move(center_prev_y[1],center_prev_y[0],center_y[1],center_y[0]) and Move(center_prev_r[1],center_prev_r[0],center_r[1],center_r[0]))==False):
        if not white_motion:
            first_move[0] = 3
        else:
            first_move[0] = 1
        if not yellow_motion:
            first_move[1] = 3
        else:
            first_move[1] = 1
        if not red_motion:
            first_move[2] = 3
        else:
            first_move[2] = 1
        if delete_flag == False:
            max_vel_y,max_vel_w,max_vel_r = demo(frame,i,data_w,data_y,data_r,velocity_w,velocity_y,velocity_r,max_vel_y,max_vel_w,max_vel_r,first_move,touch,points)
    else:
        delete_flag = True
        NoMotion_flag = True

    if (delete_flag):
        if(NoMove(center_prev_w[1],center_prev_w[0],center_w[1],center_w[0]) and NoMove(center_prev_y[1],center_prev_y[0],center_y[1],center_y[0]) and NoMove(center_prev_r[1],center_prev_r[0],center_r[1],center_r[0])):
            #imS = cv2.resize(frame, (1200, 706))
            cv2.imshow('final', cv2.cvtColor(frame, cv2.COLOR_HSV2BGR))
        else:
            delete_flag = False

    i = i + 1

    print(i-1,"--- %s seconds ---" % (time.time() - start_time))
    if cv2.waitKey(1) and 0xFF == ord("q"):
        break
cap.release()
cv2.destroyAllWindows()
