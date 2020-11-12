import numpy as np
import cv2
import glob
import math
import argparse
import timeit


ap = argparse.ArgumentParser()
ap.add_argument("-v", "--video",
	help="path to the (optional) video file")
args = vars(ap.parse_args())

cap = cv2.VideoCapture(args["video"])

def rotate_image(image, angle):
  image_center = tuple(np.array(image.shape[1::-1]) / 2)
  rot_mat = cv2.getRotationMatrix2D(image_center, angle, 1.0)
  result = cv2.warpAffine(image, rot_mat, image.shape[1::-1], flags=cv2.INTER_LINEAR)
  return result
# termination criteria
criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)

# prepare object points, like (0,0,0), (1,0,0), (2,0,0) ....,(6,5,0)
objp = np.zeros((7*15,3), np.float32)
objp[:,:2] = np.mgrid[0:15,0:7].T.reshape(-1,2)

# Arrays to store object points and image points from all the images.
objpoints = [] # 3d point in real world space
imgpoints = [] # 2d points in image plane.

img = cv2.imread('image.jpg')

cv2.imwrite('alignment/1_original.png',img)
gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)

# Find the chess board corners
ret, corners = cv2.findChessboardCorners(gray, (15,7),None)

# If found, add object points, image points (after refining them)
if ret == True:
    objpoints.append(objp)

    corners2 = cv2.cornerSubPix(gray,corners,(11,11),(-1,-1),criteria)

    imgpoints.append(corners2)

    # Draw and display the corners
    img = cv2.drawChessboardCorners(img, (15,7), corners2,ret)
    cv2.imwrite('alignment/2_calibration_points.png',img)
    cv2.imshow('img',img)
    cv2.waitKey()


ret, mtx, dist, rvecs, tvecs = cv2.calibrateCamera(objpoints, imgpoints, gray.shape[::-1],None,None)

img = cv2.imread('image.jpg')
h,  w = img.shape[:2]
newcameramtx, roi=cv2.getOptimalNewCameraMatrix(mtx,dist,(w,h),1,(w,h))
mapx,mapy = cv2.initUndistortRectifyMap(mtx,dist,None,newcameramtx,(w,h),5)
while(1):
	start = timeit.default_timer()
	ret, img2 = cap.read()

	# undistort

	#dst = cv2.remap(img2,mapx,mapy,cv2.INTER_LINEAR)

	dst = cv2.undistort(img2, mtx, dist, None, newcameramtx)
	#
	# crop the image
	x,y,w,h = roi
	dst = dst[y:y+h, x:x+w]

	dst=cv2.resize(dst,(1200,700))
	img2=cv2.resize(img2,(1200,700))
	cv2.imwrite('calibresult.png',dst)
	cv2.imshow('dst',dst)
	cv2.imshow('img2',img2)
	k = cv2.waitKey(30) & 0xff
	if k == 27:
		break
	stop = timeit.default_timer()
	print('Time: ', stop - start)

cv2.destroyAllWindows()
