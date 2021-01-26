def side_touch(center_w,velocity_w_x,velocity_w_y,center_y,velocity_y_x,velocity_y_y,center_r,velocity_r_x,velocity_r_y,i,touch,points):
    fps = 30
    ppm_x = 550
    ppm_y = 637
    next_white = [0,0]
    next_yellow = [0,0]
    next_red = [0,0]
    touch_point_w = [0,0]
    touch_point_y = [0,0]
    touch_point_r = [0,0]

    side_touch_w = False
    side_touch_y = False
    side_touch_r = False

    touch_x = 0
    touch_y = 0

    ball_radius = 20 #pixels

    next_white[1] = center_w[1] + velocity_w_x[i] * ppm_x * (1/fps)
    next_white[0] = center_w[0] + velocity_w_y[i] * ppm_y * (1 / fps)
    next_yellow[1] = center_y[1] + velocity_y_x[i] * ppm_x * (1 / fps)
    next_yellow[0] = center_y[0] + velocity_y_y[i] * ppm_y * (1 / fps)
    next_red[1] = center_r[1] + velocity_r_x[i] * ppm_x * (1 / fps)
    next_red[0] = center_r[0] + velocity_r_y[i] * ppm_y * (1 / fps)
    #print(center_w,center_y,center_r)
    #print(next_white, next_yellow, next_red)
    if next_white[0] < 160 + ball_radius or next_white[1] < 140 + ball_radius or next_white[0] > 1760 - ball_radius or next_white[1] > 940 - ball_radius:
        if (next_white[1]-center_w[1]) != 0:
            slope_w = (next_white[1]-center_w[1])/(next_white[0]-center_w[0])
            b_w = (next_white[0]*center_w[1] - center_w[0]*next_white[1])/(next_white[0]-center_w[0])
            if next_white[0] < 160 + ball_radius:
                touch_point_w[0] = round(slope_w * 160 + b_w)+round(ball_radius*slope_w)
                touch_point_w[1] = 160
                touch_y = touch_point_w[1] - 160
                touch_x = touch_point_w[0] - 140
            elif next_white[0] > 1760 - ball_radius:
                touch_point_w[0] = round(slope_w * 1760 + b_w)-round(ball_radius*slope_w)
                touch_point_w[1] = 1760
                touch_y = touch_point_w[1] - 160
                touch_x = touch_point_w[0] - 140
            elif next_white[1] < 140 + ball_radius:
                touch_point_w[1] = round((140 - b_w)/slope_w)-round(ball_radius*(-1/slope_w))
                touch_point_w[0] = 140
                touch_x = touch_point_w[0] - 140
                touch_y = touch_point_w[1] - 160
            else:
                touch_point_w[1] = round((940 - b_w)/slope_w)+round(ball_radius*(-1/slope_w))
                touch_point_w[0] = 940
                touch_x = touch_point_w[0] - 140
                touch_y = touch_point_w[1] - 160
            point_x_w = touch_x / 20
            point_y_w = touch_y / 20
            print(point_x_w, point_y_w)
            if point_x_w == 0 or point_x_w == 40:
                points.append(point_y_w)
            else:
                points.append(point_x_w)
            side_touch_w = True
        touch.append(touch_point_w)

    if next_yellow[0] < 160 + ball_radius or next_yellow[1] < 140 + ball_radius or next_yellow[0] > 1760 - ball_radius or next_yellow[1] > 940 - ball_radius:
        if (next_yellow[0] - center_y[0]) != 0:
            slope_y = (next_yellow[1] - center_y[1]) / (next_yellow[0] - center_y[0])
            b_y = (next_yellow[0] * center_y[1] - center_y[0] * next_yellow[1]) / (next_yellow[0] - center_y[0])
            if next_yellow[0] < 160 + ball_radius:
                touch_point_y[0] = round(slope_y * 160 + b_y)+round(ball_radius*slope_y)
                touch_point_y[1] = 160
                touch_y = touch_point_y[1] - 160
                touch_x = touch_point_y[0] - 140
            elif next_yellow[0] > 1760 - ball_radius:
                touch_point_y[0] = round(slope_y * 1760 + b_y)-round(ball_radius*slope_y)
                touch_point_y[1] = 1760
                touch_y = touch_point_y[1] - 160
                touch_x = touch_point_y[0] - 140
            elif next_yellow[1] < 140 + ball_radius:
                touch_point_y[1] = round((140 - b_y)/slope_y)-round(ball_radius*(-1/slope_y))
                touch_point_y[0] = 140
                touch_x = touch_point_y[0] - 140
                touch_y = touch_point_y[1] - 160
            else:
                touch_point_y[1] = round((940 - b_y)/slope_y)+round(ball_radius*(-1/slope_y))
                touch_point_y[0] = 940
                touch_x = touch_point_y[0] - 140
                touch_y = touch_point_y[1] - 160
            point_x_y = touch_x/20
            point_y_y = touch_y/20
            print(point_x_y,point_y_y)
            if point_x_y == 0 or point_x_y == 40:
                points.append(point_y_y)
            else:
                points.append(point_x_y)
            side_touch_y = True
        touch.append(touch_point_y)

    if next_red[0] < 160 + ball_radius or next_red[1] < 140 + ball_radius or next_red[0] > 1760 - ball_radius or next_red[1] > 940 - ball_radius:
        if (next_red[1] - center_r[1]) != 0:
            slope_r = (next_red[1] - center_r[1]) / (next_red[0] - center_r[0])
            b_r = (next_red[0] * center_r[1] - center_r[0] * next_red[1]) / (next_red[0] - center_r[0])
            if next_red[0] < 160 + ball_radius:
                touch_point_r[0] = round(slope_r * 160 + b_r)+round(ball_radius*slope_r)
                touch_point_r[1] = 160
                touch_y = touch_point_r[1] - 160
                touch_x = touch_point_r[0] - 140
            elif next_red[0] > 1760 - ball_radius:
                touch_point_r[0] = round(slope_r * 1760 + b_r)-round(ball_radius*slope_r)
                touch_point_r[1] = 1760
                touch_y = touch_point_r[1] - 160
                touch_x = touch_point_r[0] - 140
            elif next_red[1] < 140 + ball_radius:
                touch_point_r[1] = round((140 - b_r)/slope_r)-round(ball_radius*(-1/slope_r))
                touch_point_r[0] = 140
                touch_x = touch_point_r[0] - 140
                touch_y = touch_point_r[1] - 160
            else:
                touch_point_r[1] = round((940 - b_r)/slope_r)+round(ball_radius*(-1/slope_r))
                touch_point_r[0] = 940
                touch_x = touch_point_r[0] - 140
                touch_y = touch_point_r[1] - 160
            point_x_r = touch_x / 20
            point_y_r = touch_y / 20
            print(point_x_r, point_y_r)
            if point_x_r == 0 or point_x_r == 40:
                points.append(point_y_r)
            else:
                points.append(point_x_r)
            side_touch_r = True
        touch.append(touch_point_r)
    #print(side_touch_w,side_touch_y,side_touch_r)
    return side_touch_w,side_touch_y,side_touch_r,touch