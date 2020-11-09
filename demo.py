def demo(frame,i,data,data_w,data_y,data_r):

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
    #frame_amount = 1  #152 for 20fps & 39 for 5 fps & 43 for 5fps new & 225 for 30fps & 422 for salon data

    #data = [0] * frame_amount

    #cap = cv2.VideoCapture('zor_video.mp4')
    #fourcc = cv2.VideoWriter_fourcc(*'VIDX')
    #out = cv2.VideoWriter('C:\\Users\\fatma\\PycharmProjects\\pythonProject\\Outputs\\'+str(dateStr)+str(timeStr)+'output.mp4v',cv2.VideoWriter_fourcc(*'XVID'),60, (1920, 1080))

    #white_pos = np.loadtxt('white_center.csv', delimiter=',')
    #yellow_pos =  np.loadtxt('yellow_center.csv', delimiter=',')
    #red_pos =  np.loadtxt('red_center.csv', delimiter=',')

    #data_w.append(white_pos)
    #data_y.append(yellow_pos)
    #data_r.append(red_pos)

    #vel_w = np.loadtxt('white_velocity.csv', delimiter=',')
    #vel_y =  np.loadtxt('yellow_velocity.csv', delimiter=',')
    #vel_r =  np.loadtxt('red_velocity.csv', delimiter=',')

    #cv2.circle(frame, (int(data_w[i][0]), int(data_w[i][1])), 2, (255, 0, 0), -1)
    #cv2.circle(frame, (int(data_y[i][0]), int(data_y[i][1])), 2, (255, 0, 0), -1)
    #cv2.circle(frame, (int(data_r[i][0]), int(data_r[i][1])), 2, (255, 0, 0), -1)

    if i>0:
        for k in range(i):
            k = k + 1
            cv2.line(frame, (int(data_w[k - 1][0]),int(data_w[k - 1][1])), (int(data_w[k][0]),int(data_w[k][1])), (255, 255, 255), 3)
            cv2.line(frame, (int(data_y[k - 1][0]),int(data_y[k - 1][1])), (int(data_y[k][0]),int(data_y[k][1])), (0, 255, 255), 1)
            cv2.line(frame, (int(data_r[k - 1][0]), int(data_r[k - 1][1])), (int(data_r[k][0]), int(data_r[k][1])),
                        (0, 0, 255), 1)
    #font = cv2.FONT_HERSHEY_SIMPLEX
    #cv2.circle(frame, (40, 988), 5, (0, 255, 255), -1)
    #cv2.circle(frame, (40, 1018 ), 5, (255, 255, 255), -1)
    #cv2.circle(frame, (40, 1048), 5, (0, 0, 255), -1)
    #cv2.putText(frame, "Yellow ball speed(m/s):" + str(round(vel_y,2)) , (50, 995), font, 0.8, (255, 255, 255), 2,cv2.LINE_AA)
    #cv2.putText(frame, "White ball speed(m/s):" + str(round(vel_w,2)) , (50, 1025), font, 0.8, (255, 255, 255), 2, cv2.LINE_AA)
    #cv2.putText(frame, "Red ball speed(m/s):" + str(round(vel_r,2)) , (50, 1055), font, 0.8, (255, 255, 255), 2, cv2.LINE_AA)
    #out.write(frame)
    imS = cv2.resize(frame, (1200, 706))
    cv2.imshow('final', imS)#, cv2.waitKey(0), cv2.destroyAllWindows()



