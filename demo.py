import cv2
import numpy as np
import time
from datetime import datetime

dateTimeObj = datetime.now()
dateObj = dateTimeObj.date()
timeObj = dateTimeObj.time()
timeStr = timeObj.strftime("%H%M%S_")
dateStr = dateObj.strftime("%b%d%Y_")

start_time = time.time()
i = 0
frame_amount = 450  #152 for 20fps & 39 for 5 fps & 43 for 5fps new & 225 for 30fps & 422 for salon data

data = [0] * frame_amount

cap = cv2.VideoCapture('video4.mp4')
fourcc = cv2.VideoWriter_fourcc(*'VIDX')
out = cv2.VideoWriter('C:\\Users\\fatma\\PycharmProjects\\pythonProject\\Outputs\\'+str(dateStr)+str(timeStr)+'output.mp4v',cv2.VideoWriter_fourcc(*'XVID'),60, (1920, 1080))

data_w = np.loadtxt('white_center.csv', delimiter=',')
data_y =  np.loadtxt('yellow_center.csv', delimiter=',')
data_r =  np.loadtxt('red_center.csv', delimiter=',')
vel_w = np.loadtxt('white_velocity.csv', delimiter=',')
vel_y =  np.loadtxt('yellow_velocity.csv', delimiter=',')
vel_r =  np.loadtxt('red_velocity.csv', delimiter=',')

while(i<frame_amount-1):

    ret, data[i] = cap.read()

    out.write(data[i])
    img_y = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
    img_x = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)

    cv2.circle(data[i], (int(data_w[i][0]),int(data_w[i][1])),2,(255, 0, 0), -1)
    cv2.circle(data[i], (int(data_y[i][0]), int(data_y[i][1])), 2, (255, 0, 0), -1)
    cv2.circle(data[i], (int(data_r[i][0]), int(data_r[i][1])), 2, (255, 0, 0), -1)

    for k in range(i-2):
        k=k+2
        cv2.line(data[i], (int(data_w[k - 1][0]),int(data_w[k - 1][1])), (int(data_w[k][0]),int(data_w[k][1])), (255, 255, 255), 1)
        #print((int(data_w[k - 1][0]),int(data_w[k - 1][1])), (int(data_w[k][0]),int(data_w[k][1])))
        cv2.line(data[i], (int(data_y[k - 1][0]),int(data_y[k - 1][1])), (int(data_y[k][0]),int(data_y[k][1])), (0, 255, 255), 3)
        cv2.line(data[i], (int(data_r[k - 1][0]), int(data_r[k - 1][1])), (int(data_r[k][0]), int(data_r[k][1])),
                (0, 0, 255), 1)
    font = cv2.FONT_HERSHEY_SIMPLEX
    cv2.circle(data[i], (40, 988), 5, (0, 255, 255), -1)
    cv2.circle(data[i], (40, 1018 ), 5, (255, 255, 255), -1)
    cv2.circle(data[i], (40, 1048), 5, (0, 0, 255), -1)
    cv2.putText(data[i], "Yellow ball speed(m/s):" + str(round(vel_y[i], 2)) , (50, 995), font, 0.8, (255, 255, 255), 2,cv2.LINE_AA)
    cv2.putText(data[i], "White ball speed(m/s):" + str(round(vel_w[i],2)) , (50, 1025), font, 0.8, (255, 255, 255), 2, cv2.LINE_AA)
    cv2.putText(data[i], "Red ball speed(m/s):" + str(round(vel_r[i],2)) , (50, 1055), font, 0.8, (255, 255, 255), 2, cv2.LINE_AA)
    out.write(data[i])
    imS = cv2.resize(data[i], (1200, 706))
    cv2.imshow('final', imS)#, cv2.waitKey(0), cv2.destroyAllWindows()

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    i = i + 1

out.release()
cap.release()