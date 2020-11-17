
def NoMove(xi,yi,xf,yf):
    z = abs(xi - xf)
    t = abs(yi - yf)
    w = z**2+t**2
    if w < 9:
        # print("No Motion Detected!")
        return True
    else:
        # print("Motion Detected! New coordinates of the ball: ", yf,",", xf)
        return False
def Move(xi,yi,xf,yf):
    if xi == xf and yi == yf:
        # print("No More Movement! ")
        return True
    else:
        # print("New Coordinates:",yf,",",xf)
        return False

def Move_all(y,w,r):
    if y == False and w == False and r== False:
        print("All balls are on the move")
        return True
    elif y == False and w == False and r == True:
        print("Yellow ball and White ball are on the move...")
        return True
    elif y == True and w == False and r == False:
        print("White Ball and Red Ball are on the move...")
        return True
    elif y == False and w == True and r == False:
        print("Yellow Ball and Red Ball are on the move...")
        return True
    elif y == False and w == True and r == True:
        print("Yellow ball is on the move...")
        return True
    elif y == True and w == False and r == True:
        print("White ball is on the move...")
        return True
    elif y == True and w == True and r == False:
        print("Red ball is on the move...")
        return True
    elif y == True and w == True and r == True:
        print("No movement Detected")
        return False






