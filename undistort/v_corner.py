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

video = cv2.VideoCapture(args["video"])
if (video.isOpened() == False):
	print("Error reading video file")
frame_width = int(video.get(3))
frame_height = int(video.get(4))
x,y,w,h = roi
size = (1300, 700)

# Below VideoWriter object will create
# a frame of above defined The output
# is stored in 'filename.avi' file.
result = cv2.VideoWriter('filename.mp4',
						 cv2.VideoWriter_fourcc(*'MP4V'),
						 30, size)
while(1):
	start = timeit.default_timer()
	ret, img2 = video.read()
	if ret == True:
		# undistort

		#dst = cv2.remap(img2,mapx,mapy,cv2.INTER_LINEAR)

		dst = cv2.undistort(img2.copy(), mtx, dist, None, newcameramtx)
		#
		# crop the image
		x,y,w,h = roi
		dst = dst[y:y+h, x:x+w]
		dst = cv2.resize(dst,(1300,700))
		cv2.imshow('dst',dst)
		result.write(dst)
		if cv2.waitKey(1) & 0xFF == ord('s'):
			break
	else:
		break
	stop = timeit.default_timer()
	print('Time: ', stop - start)
video.release()
result.release()
print("The video was successfully saved")
