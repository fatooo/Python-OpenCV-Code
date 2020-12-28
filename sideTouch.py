def side_touch(center_w,velocity_w_x,velocity_w_y,center_y,velocity_y_x,velocity_y_y,center_r,velocity_r_x,velocity_r_y,i,touch):
    fps = 30
    ppm_x = 550
    ppm_y = 637
    next_white = [0,0]
    next_yellow = [0,0]
    next_red = [0,0]

    side_touch_w = False
    side_touch_y = False
    side_touch_r = False

    ball_radius = 18 #pixels

    next_white[0] = center_w[0] + velocity_w_y[i] * ppm_y * (1/fps)
    next_white[1] = center_w[1] + velocity_w_x[i] * ppm_x * (1 / fps)
    next_yellow[0] = center_y[0] + velocity_y_y[i] * ppm_y * (1 / fps)
    next_yellow[1] = center_y[1] + velocity_y_x[i] * ppm_x * (1 / fps)
    next_red[0] = center_r[0] + velocity_r_y[i] * ppm_y * (1 / fps)
    next_red[1] = center_r[1] + velocity_r_x[i] * ppm_x * (1 / fps)
    print(center_w,center_y,center_r)
    print(next_white, next_yellow, next_red)
    if next_white[0] < 160 + ball_radius or next_white[1] < 140 + ball_radius or next_white[0] > 1760 - ball_radius or next_white[1] > 940 - ball_radius:
        side_touch_w = True
        touch.append(center_w)

    if next_yellow[0] < 160 + ball_radius or next_yellow[1] < 140 + ball_radius or next_yellow[0] > 1760 - ball_radius or next_yellow[1] > 940 - ball_radius:
        side_touch_y = True
        touch.append(center_y)

    if next_red[0] < 160 + ball_radius or next_red[1] < 140 + ball_radius or next_red[0] > 1760 - ball_radius or next_red[1] > 940 - ball_radius:
        side_touch_r = True
        touch.append(center_y)
    print(side_touch_w,side_touch_y,side_touch_r)
    return side_touch_w,side_touch_y,side_touch_r,touch