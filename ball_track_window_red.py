def red_track(frame,i,data,data_r,template_o,x_prime,y_prime,velocity_x,velocity_y,velocity,x_start,y_start,x_stop,y_stop):

    import cv2
    import numpy as np
    import time
    import math
    from datetime import datetime

    dateTimeObj = datetime.now()
    dateObj = dateTimeObj.date()
    timeObj = dateTimeObj.time()
    timeStr = timeObj.strftime("%H%M%S_")
    dateStr = dateObj.strftime("%b%d%Y_")

    start_time = time.time()

    big_templates = []
    initial_window = 250
    fps = 30 #frames per second
    ppm_x = 550 #pixel per meter for x axis
    ppm_y = 637 #pixel per meter for y axis
    w = initial_window
    #template_o = cv2.imread('C:\\Users\\fatma\\PycharmProjects\\pythonProject\\Templates\\deneme_white.png')
    template_2_o = cv2.imread('C:\\Users\\fatma\\PycharmProjects\\pythonProject\\Templates\\red_2.png')

    template = np.float32(template_o)
    template_2= np.float32(template_2_o)

    template_x = template.shape[0]
    template_y = template.shape[1]

    template_x_2 = template_2.shape[0]
    template_y_2 = template_2.shape[1]

    frame_amount = 1  #152 for 20fps & 39 for 5 fps & 43 for 5fps new & 225 for 30fps & 422 for salon data

    method = cv2.TM_SQDIFF_NORMED  #method used to check the correlation between the template and the frame
    #data.append(frame)
    #min_val = [0] * frame_amount
    #max_val = [0] * frame_amount
    #min_loc = [[0] * 2 for i in range(frame_amount)]
    #max_loc = [[0] * 2 for i in range(frame_amount)]

    #min_val_2 = [0] * frame_amount
    #max_val_2 = [0] * frame_amount
    #min_loc_2 = [[0] * 2 for i in range(frame_amount)]
    #max_loc_2 = [[0] * 2 for i in range(frame_amount)]

    #x_prime = [0] * frame_amount
    #y_prime = [0] * frame_amount

    #velocity = [0] * frame_amount
    #velocity_x = [0] * frame_amount
    #velocity_y = [0] * frame_amount

    #center = np.ndarray(shape=(1,frame_amount,2))
    #center_prev = [0]*frame_amount

    #data = [0] * frame_amount

    #cap = cv2.VideoCapture('zor_video.mp4')
    #fourcc = cv2.VideoWriter_fourcc(*'XVID')
    #out = cv2.VideoWriter('output.avi', fourcc, 30.0, (768,576))

    if (i>-1):

        #ret, data[i] = cap.read()
        #out.write(data[i])
        #img_y = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
        #img_x = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
        img_y = 1920
        img_x = 1080

        half_window = w/2
        if i == 0:
            img_crop = data[0]
        elif i == 1:
            if y_prime[i - 1] - half_window < 0:
                y_start = 0 #+ ((velocity_y[i-1] / (fps)) * ppm_y)
            else:
                fato = y_prime[i-1]
                y_start = y_prime[i - 1] - half_window #+ ((velocity_y[i-1] / (fps)) * ppm_y)
            if x_prime[i - 1] - half_window < 0:
                x_start = 0 #+ ((velocity_x[i-1] / (fps)) * ppm_x)
            else:
                x_start = x_prime[i - 1] - half_window #+ ((velocity_x[i-1] / (fps)) * ppm_x)
            if y_prime[i - 1] + half_window > img_y:
                y_stop = img_y
            else:
                y_stop = y_start + w
            if x_prime[i - 1] + half_window > img_x:
                x_stop = img_x
            else:
                x_stop = x_start + w
            #print(velocity_x[i] / fps * ppm_x, velocity_y[i] / fps * ppm_y)
            #print(x_start, x_stop, y_start, y_stop)
            img_crop = frame[round(x_start):round(x_stop), round(y_start):round(y_stop)]
        else:
            if x_start + ((velocity_x[i - 1] / (fps)) * ppm_x) < 0:
                x_start = 0
            else:
                x_start = x_start + ((velocity_x[i - 1] / (fps)) * ppm_x)
            if x_start + w > img_x:
                x_stop = img_x
            else:
                x_stop = x_start + w
            if y_start + ((velocity_y[i - 1] / (fps)) * ppm_y) < 0:
                y_start = 0
            else:
                y_start = y_start + ((velocity_y[i - 1] / (fps)) * ppm_y)
            if y_start + w > img_y:
                y_stop = img_y
            else:
                y_stop = y_start + w
            #print(((velocity_x[i-1] / (fps)) * ppm_x),((velocity_y[i-1] / (fps)) * ppm_y))

            #print(velocity_x[i]/ fps * ppm_x,velocity_y[i]/fps * ppm_y)
            #print(x_start[0],x_stop,y_start,y_stop)
            img_crop = frame[round(x_start):round(x_stop), round(y_start):round(y_stop)]
            #cv2.rectangle(data[i], (int(y_start), int(x_start)), (int(y_stop), int(x_stop)), (0, 255, 0), 2)
            #imS = cv2.resize(data[i], (960, 540))
            #cv2.imshow('crop',imS),cv2.waitKey(0), cv2.destroyAllWindows()
        img_crop_o = img_crop
        img_crop = np.float32(img_crop)
        if i>0 and velocity[i-1]<1.0:
            template = template_2
        #cv2.imshow('crop', template_o), cv2.waitKey(0), cv2.destroyAllWindows()
        res = cv2.matchTemplate(img_crop, template, method)
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)

        est_x = round(min_loc[1])
        est_y = round(min_loc[0])

        #cv2.circle(img_crop_o,(est_y+round(template_y/2), est_x+round(template_x/2)),2,(255, 0, 0), -1)
        #cv2.imshow('crop', img_crop_o), cv2.waitKey(0), cv2.destroyAllWindows()
        if i == 0:
            x_prime.append(est_x)

            y_prime.append(est_y)
        else:
            if x_prime[i - 1] - half_window < 0:
                x_prime.append(x_prime[i - 1] - half_window + est_x + (half_window - x_prime[i - 1]))
            else:
                x_prime.append(x_prime[i - 1] - half_window + est_x)
            if y_prime[i - 1] - half_window < 0:
                y_prime.append(y_prime[i - 1] - half_window + est_y + (half_window - y_prime[i - 1]))
            else:
                y_prime.append(y_prime[i - 1] - half_window + est_y)

        #print(i,y_prime[i], x_prime[i])

        template_o = frame[int(x_prime[i]):int(x_prime[i])+template_x, int(y_prime[i]):int(y_prime[i])+template_y] #update the template with the ball found in the current frame
        #template_o = cv2.GaussianBlur(template_o, (5, 5), -1)

            #print(template_x, template_y)
        #big_templates.append(template_o)

        template = np.float32(template_o)
        res_2 = cv2.matchTemplate(template, template_2, method)

        min_val_2, max_val_2, min_loc_2, max_loc_2 = cv2.minMaxLoc(res_2)

        #cv2.circle(template_o, (round(min_loc_2[i][0]+1) + round(template_y_2 / 2), round(min_loc_2[i][1]) + round(template_x_2 / 2)), 2,
                       #(0, 0, 255), -1)
        #rect = cv2.rectangle(template_o, (int(min_loc_2[i][0]+2), int(min_loc_2[i][1])),
                                 #(int(min_loc_2[i][0] + template_y_2), int(min_loc_2[i][1] + template_x_2)), (0, 255, 0), 1)
        #cv2.imshow('final', template_o), cv2.waitKey(0), cv2.destroyAllWindows()


        x_prime[i] = round(x_prime[i] + template_x / 2 + min_loc_2[1]) #used for double template matching
        y_prime[i] = round(y_prime[i] + template_y / 2 + min_loc_2[0])

        #print(min_loc_2[i][1], min_loc_2[i][0])
        center_prev = (
                round(y_prime[i - 1] - (round(template_y / 2) - round(template_y_2 / 2))),
                round(x_prime[i - 1] - (round(template_x / 2) - round(template_x_2 / 2))))

        center = (round(y_prime[i] - (round(template_y / 2) - round(template_y_2 / 2))),
                round(x_prime[i] - (round(template_x / 2) - round(template_x_2 / 2))))
        #print(center[i])

        velocity_x.append((center[1] - center_prev[1]) * fps / ppm_x)
        velocity_y.append((center[0] - center_prev[0]) * fps / ppm_y)
        velocity.append(math.sqrt(math.pow(abs(velocity_x[i]), 2) + math.pow(abs(velocity_y[i]), 2)))
        #print(velocity[i])

        cv2.circle(frame, (int(center[0]), int(center[1])), 0, (0, 255, 0), 10)

        #imS = cv2.resize(frame, (1200, 706))
        #cv2.imshow('final', imS), cv2.waitKey(0), cv2.destroyAllWindows()
        #if cv2.waitKey(1) & 0xFF == ord('q'):
            #break

    velocity[0] = 0
    # np.savetxt("C:\\Users\\fatma\\PycharmProjects\\pythonProject\\Position and Velocity Data\\"+str(dateStr)+str(timeStr)+'white_center.csv', center[0], delimiter=",")
    # np.savetxt("C:\\Users\\fatma\\PycharmProjects\\pythonProject\\Position and Velocity Data\\"+str(dateStr)+str(timeStr)+'white_velocity.csv', velocity, delimiter=",",fmt='%f')
    #np.savetxt("white_center.csv", center, delimiter=",")
    np.savetxt("red_velocity.csv", velocity, delimiter=",",fmt='%f')
    #print("--- %s seconds ---" % (time.time() - start_time))
    data_r.append(center)
    return template_o,velocity_x,velocity_y,velocity,data,data_r,x_start,y_start,x_stop,y_stop,center_prev,center

