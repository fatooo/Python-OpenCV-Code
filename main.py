from ball_track_window_white import white_track
from ball_track_window_yellow import yellow_track
from ball_track_window_red import red_track
from fish_eye_correct import fish_eye_correct
from demo import demo
import cv2
from datetime import datetime
from movefunction import Move
from movefunction import NoMove

dateTimeObj = datetime.now()
dateObj = dateTimeObj.date()
timeObj = dateTimeObj.time()
timeStr = timeObj.strftime("%H%M%S_")
dateStr = dateObj.strftime("%b%d%Y_")

#import the big templates for each ball
template_w = cv2.imread('C:\\Users\\fatma\\PycharmProjects\\pythonProject\\Templates\\deneme_white.png')
template_y = cv2.imread('C:\\Users\\fatma\\PycharmProjects\\pythonProject\\Templates\\yellow_big_2.png')
template_r = cv2.imread('C:\\Users\\fatma\\PycharmProjects\\pythonProject\\Templates\\red_big_2.png')
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

i = 0
max_vel_y = 0
max_vel_w = 0
max_vel_r = 0

NoMotion_flag = True
delete_flag = False
#template_w,template_y,template_r = templateFind(); //find initial big templates

while(True):

    ret, frame = cap.read()
    data.append(frame)
    #out.write(frame)
    #frame = fish_eye_correct(frame) //fish eye correct the current frame
    template_w,velocity_x_w,velocity_y_w,velocity_w,data,data_w,x_start_w,y_start_w,x_stop_w,y_stop_w,center_prev_w,center_w = white_track(frame,i,data,data_w,template_w,x_prime_w,y_prime_w,velocity_x_w,velocity_y_w,velocity_w,x_start_w,y_start_w,x_stop_w,y_stop_w)
    template_y,velocity_x_y,velocity_y_y,velocity_y,data,data_y,x_start_y,y_start_y,x_stop_y,y_stop_y,center_prev_y,center_y = yellow_track(frame,i,data,data_y,template_y,x_prime_y,y_prime_y,velocity_x_y,velocity_y_y,velocity_y,x_start_y,y_start_y,x_stop_y,y_stop_y)
    template_r,velocity_x_r,velocity_y_r,velocity_r,data,data_r,x_start_r,y_start_r,x_stop_r,y_stop_r,center_prev_r,center_r = red_track(frame,i,data,data_r,template_r,x_prime_r,y_prime_r,velocity_x_r,velocity_y_r,velocity_r,x_start_r,y_start_r,x_stop_r,y_stop_r)

    if NoMotion_flag:
        NoMotion_flag = NoMove(center_prev_w[1],center_prev_w[0],center_w[1],center_w[0]) and NoMove(center_prev_y[1],center_prev_y[0],center_y[1],center_y[0]) and NoMove(center_prev_r[1],center_prev_r[0],center_r[1],center_r[0])

    if (NoMotion_flag==True) or ((Move(center_prev_w[1],center_prev_w[0],center_w[1],center_w[0]) and Move(center_prev_y[1],center_prev_y[0],center_y[1],center_y[0]) and Move(center_prev_r[1],center_prev_r[0],center_r[1],center_r[0]))==False):
        if delete_flag == False:
            max_vel_y,max_vel_w,max_vel_r = demo(frame,i,data,data_w,data_y,data_r,velocity_w,velocity_y,velocity_r,max_vel_y,max_vel_w,max_vel_r)
    else:
        delete_flag = True
        NoMotion_flag = True

    if (delete_flag):
        if(NoMove(center_prev_w[1],center_prev_w[0],center_w[1],center_w[0]) and NoMove(center_prev_y[1],center_prev_y[0],center_y[1],center_y[0]) and NoMove(center_prev_r[1],center_prev_r[0],center_r[1],center_r[0])):
            imS = cv2.resize(frame, (1200, 706))
            cv2.imshow('final', imS)
        else:
            delete_flag = False
    
    i = i + 1
    if cv2.waitKey(1) and 0xFF == ord("q"):
        break
cap.release()
cv2.destroyAllWindows()
