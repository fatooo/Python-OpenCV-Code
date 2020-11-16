# encoding:utf-8
"""
---Fonksiyon Tanımları---

cueStickDetector: Istakayı tanımlar ve izlerini kaydeder.
drawBorders: Bilardo masasındaki; iç havuz, dış havuz ve topun yarı çapı kadar daha içeride olmak üzere 3 adet çerçeve çizer. Masadaki koordinat noktalarını belirtir.

old Runtimes :
old cueStickDetector Time:  0.04839320000000047
drawBorders Time:  0.0037850999999999857 (Artık kullanılmıyor)

Runtimes now:
cueStickDetector Time:  0.04142960000000073

"""

# -- Libraries -- #
import numpy as np
import cv2
import argparse
import timeit
import math

ap = argparse.ArgumentParser()
ap.add_argument("-v", "--video",
	help="path to the (optional) video file")
args = vars(ap.parse_args())

cap = cv2.VideoCapture(args["video"])

class Billiards:
	def __init__(self):
		# -- Parameters and variables -- #

		# This value decides how much pixels cropped from the frame, to prevent frame to be splitted,
		# FrameCropped
		self.FraC = 50

		# HSV Colour Range - These values need to be changed depending on the feed

		self.lower_blue = np.array([99,137,170])
		self.upper_blue = np.array([180,219,250])

		#self.lower_blue = np.array([84,0,0])
		#self.upper_blue = np.array([180,140,255])

		# Rectangle Paramaters
		self.rectangle_flag = 0
		self.x , self.y, self.w, self.h = 0,0,0,0
		self.RectCol=(255,255,100)

		# Coordinate Points Parameters
		self.PointCol = (0,0,255)
		self.cPointsFlag = 0

		# Pool Edge Width
		self.pew = 14

		# Ball Radius
		self.br = 13

		# Coordinate point interval
		self.cpi = 52

		# Cue Stick Track Colour
		self.cueTrackCol = (255,0,255)

		# Houhlines function parameter, decides min length of a line to be detected
		self.minLineLength = 100

		# Edge Detection Parameters
		self.lower = 131
		self.upper = 196

		self.scale = 0.6
		self.firstFrameObtained = False
		self.drawing = False
		self.ix = -1
		self.iy = -1
		self.rectangle_stop = 0
		self.line_stop = 0
		self.x_global = 0
		self.y_global = 0
		self.mode = 0
		self.line_edge_points = []
		print("Class initialized...")

	# mouse callback function
	def mouseCallback(self,event,x,y,flags,param):
		if event == cv2.EVENT_LBUTTONDOWN:
			self.line_stop = 0
			self.rectangle_stop = 0
			self.drawing = True
			self.ix,self.iy = x,y
			if self.mode == 0:
				self.line_edge_points.append((x,y))
				cv2.circle(self.frame_img2,(x,y),4,(0,0,255),-1)

		elif event == cv2.EVENT_MOUSEMOVE:
			center = (x,y)
			self.zoomed = self.__zoom(self.frame_img_rot,center)
			self.zoomed = self.__zoom(self.frame_img3,center)

			if self.drawing == True:
				if self.mode == 1:
					cv2.rectangle(self.frame_img_rot2,(self.ix,self.iy),(x,y),(0,255,0),2)
					self.zoomed = self.__zoom(self.frame_img_rot2,center)
					self.rectangle_stop = 1
				else:
					cv2.line(self.frame_img3,(self.ix,self.iy),(x,y),(0,255,0),1)
					self.zoomed = self.__zoom(self.frame_img3,center)
					self.line_stop = 1
				self.x_global,self.y_global = x,y

		elif event == cv2.EVENT_LBUTTONUP:
			self.drawing = False
			if self.mode == 1:
				cv2.rectangle(self.frame_img_rot,(self.ix,self.iy),(x,y),(0,255,0),2)
			else:
				cv2.line(self.frame_img2,(self.ix,self.iy),(x,y),(0,255,0),1)
				self.line_edge_points.append((x,y))
				cv2.circle(self.frame_img2,(x,y),4,(0,255,255),-1)

	def __zoom(self, img, center2=None):
		img = cv2.resize(img,(500,500))
		# actual function to zoom
		height, width = img.shape[:2]
		x,y = center2
		center = ((width/self.frame_img.shape[1])*x,(height/self.frame_img.shape[0])*y)
		xi,yi = center
		cv2.circle(img,(int(xi),int(yi)),1,(0,255,255),-1)

		if center is None:
			#   Calculation when the center value is the initial value
			center_x = int(width / 2)
			center_y = int(height / 2)
			radius_x, radius_y = int(width / 2), int(height / 2)
		else:
			#   Calculation at a specific location
			rate = height / width
			center_x, center_y = center

		#   Calculate centroids for ratio range
		if center_x < width * (1-rate):
			center_x = width * (1-rate)
		elif center_x > width * rate:
			center_x = width * rate
		if center_y < height * (1-rate):
			center_y = height * (1-rate)
		elif center_y > height * rate:
			center_y = height * rate

		center_x, center_y = int(center_x), int(center_y)
		left_x, right_x = center_x, int(width - center_x)
		up_y, down_y = int(height - center_y), center_y
		radius_x = min(left_x, right_x)
		radius_y = min(up_y, down_y)

		# Actual zoom code
		radius_x, radius_y = int(self.scale * radius_x), int(self.scale * radius_y)

		# size calculation
		min_x, max_x = center_x - radius_x, center_x + radius_x
		min_y, max_y = center_y - radius_y, center_y + radius_y

		# Crop image to size
		cropped = img[min_y:max_y, min_x:max_x]
		# Return to original size
		new_cropped = cv2.resize(cropped, (width, height))

		return new_cropped

	def frame_creater(self,img):
		self.frame_img = img.copy()
		self.zoomed = img.copy()
		self.zoomed2 = self.zoomed.copy()
		#self.frame_img = cv2.resize(self.frame_img,(1400,700))
		self.frame_img2 = self.frame_img.copy()
		self.frame_img3 = self.frame_img.copy()
		self.frame_img_rot = self.frame_img.copy()
		self.frame_img_rot2 = self.frame_img_rot.copy()
		while(1):
			if self.rectangle_stop == 1:
				cv2.rectangle(self.frame_img3,(self.ix,self.iy),(self.x_global,self.y_global),(0,255,0),1)

			if self.line_stop == 1:
				cv2.line(self.frame_img3,(self.ix,self.iy),(self.x_global,self.y_global),(0,255,0),1)

			if len(self.line_edge_points) == 2:
				center = self.line_edge_points[0]
				self.frameAngle = (180/math.pi)*math.atan((self.line_edge_points[1][1] - self.line_edge_points[0][1]) / (self.line_edge_points[1][0] - self.line_edge_points[0][0]))
				#print(angle)
				self.frameCenter = tuple(map(int, center))
				# get row and col num in self.frame_img
				self.frameHeight, self.frameWidth = self.frame_img.shape[0], self.frame_img.shape[1]
				# calculate the rotation matrself.ix
				self.rotationMatrix = cv2.getRotationMatrix2D(self.frameCenter, self.frameAngle, 1)
				print("self.frameAngle",self.frameAngle)
				# rotate the original image
				self.frame_img_rot = cv2.warpAffine(self.frame_img.copy(), self.rotationMatrix, (self.frameWidth, self.frameHeight))

			cv2.imshow('self.zoomed',self.zoomed)
			cv2.imshow('image',self.frame_img3)
			self.frame_img3=self.frame_img2.copy()
			k = cv2.waitKey(1) & 0xFF
			if k == 27:
				break

		cv2.imshow('self.frame_img_rot',self.frame_img_rot)
		cv2.waitKey()

		self.mode = 1
		while(1):
			if self.rectangle_stop == 1:
				cv2.rectangle(self.frame_img_rot2,(self.ix,self.iy),(self.x_global,self.y_global),(0,255,0),2)
			cv2.imshow('self.zoomed',self.zoomed)
			cv2.imshow('image',self.frame_img_rot2)
			self.frame_img_rot2=self.frame_img_rot.copy()
			k = cv2.waitKey(1) & 0xFF
			if k == 27:
				break
		cv2.destroyAllWindows()

	def cueStickDetector(self):
		total_lines = []
		while(1):
			start = timeit.default_timer()
			ret, img = cap.read()
			if self.firstFrameObtained == False:
				self.frame_creater(img)
				self.firstFrameObtained = True

			img = cv2.warpAffine(img, self.rotationMatrix, (self.frameWidth, self.frameHeight))
			cv2.rectangle(img,(self.ix,self.iy),(self.x_global,self.y_global),self.RectCol,1)
			cv2.rectangle(img,(self.ix,self.iy),(self.x_global,self.y_global)  ,self.RectCol,1)
			cv2.rectangle(img,(self.ix+self.pew,self.iy+self.pew),(self.x_global-self.pew,self.y_global-self.pew)  ,self.RectCol,1)
			cv2.rectangle(img,(self.ix+self.pew+self.br,self.iy+self.pew+self.br),(self.x_global-self.pew-self.br,self.y_global-self.pew-self.br)  ,self.RectCol,1)
			# (1) create a copy of the original:

			# Crops the original image to pool sized image
			img2 = img[self.iy+self.FraC:self.y_global-self.FraC,self.ix+self.FraC:self.x_global-self.FraC,:]
			overlay = img2.copy()
			# (2) draw shapes:
			# Edge detection
			gray = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)
			edges = cv2.Canny(gray, self.lower, self.upper, apertureSize=3)
			# cv2.imshow('edges', edges)
			# k = cv2.waitKey(30) & 0xff
			# if k == 27:
			#     break
			# Line Detection
			lines = cv2.HoughLines(edges, 1, np.pi / 180, self.minLineLength,19)


			# Define lists
			listx1 = []
			listy1 = []

			listx2 = []
			listy2 = []
			counter = 0

			center = None
			lines2 = []
			lines3 = []

			try:
				for line in lines:

					rho,theta = line[0]
					a = np.cos(theta)
					b = np.sin(theta)
					x0 = a * rho
					y0 = b * rho
					# x1 stores the rounded off value of (r * cos(theta) - 1000 * sin(theta))
					x1 = int(x0 + 1000 * (-b))
					# y1 stores the rounded off value of (r * sin(theta)+ 1000 * cos(theta))
					y1 = int(y0 + 1000 * (a))
					# x2 stores the rounded off value of (r * cos(theta)+ 1000 * sin(theta))
					x2 = int(x0 - 1000 * (-b))
					# y2 stores the rounded off value of (r * sin(theta)- 1000 * cos(theta))
					y2 = int(y0 - 1000 * (a))
					listx1.append(x1)
					listy1.append(y1)

					listx2.append(x2)
					listy2.append(y2)
					counter +=1
					if counter == 50:
						break
					#cv2.line(img2, (x1, y1), (x2, y2), (0, 0, 255), )

				# Line detection fins two lines on two sides of cue stick
				# We find the line pass through middle of both

				midx1 = int((listx1[0] + listx1[1])/2)
				midy1 = int((listy1[0] + listy1[1])/2)

				midx2 = int((listx2[0] + listx2[1])/2)
				midy2 = int((listy2[0] + listy2[1])/2)
				linepoints = [midx1,midy1,midx2,midy2]

				# Checks if more than one line found
				if counter > 1:
					linepoints = [midx1,midy1,midx2,midy2]
					lines2.append(linepoints)
					total_lines.append(linepoints)

				counter = 0

			except:

				# Except cannot be empty :) so pl is nothing.
				pl = None

			for i in range(0, len(total_lines)):
				#cv2.circle(overlay, (133, 132), 12, (0, 255, 0), -1)
				#cv2.circle(overlay, (166, 132), 12, (0, 255, 0), -1)
				# Draw every line, on new frame
				cv2.line(overlay, (total_lines[i][0], total_lines[i][1]), (total_lines[i][2], total_lines[i][3]), self.cueTrackCol, 1)

			opacity = 0.3
			cv2.addWeighted(overlay, opacity, img2, 1 - opacity, 0, img2)

			cv2.imshow('image2', img2)

			cv2.imshow('image', img)

			k = cv2.waitKey(30) & 0xff
			if k == 27:
						break
			stop = timeit.default_timer()
			print('cueStickDetector Time: ', stop - start)

def main():
	bill = Billiards()
	cv2.namedWindow('image')
	cv2.setMouseCallback('image',bill.mouseCallback)
	bill.cueStickDetector()

	cap.release()

if __name__ == "__main__":
	main()


"""

Yapılacaklar

Koordinat sistemi.

fisheyeye ek olarak yatay ve dikeydeki noktaların y-x kordinatlarını hizalayacak ek algoritma(Gerek olmayabilir)

ıstakanın uzantıları toptan geçiyor mu kontrolcüsü

ıstaka izleri atış bittikten sonra silinmeli.

bütün değişkenler piksel türünde, onların santimetre veya metreye çevirilmesi lazım.

HSV ile dikdörtgen çizme farklı mekanlarda soruna yol açabilir,

onun yerine bir arayüz hazırlanarak dış havuz kullanıcı tarafından dikdörtgen içine alınmalı.

Farklı masa ve zemin renklerine bu şekilde adapde olunabilir.

çarpışma algılama

iki top merkezi arasndaki uzaklık yarı çaptan daha az olursa toplar çarpışmış sayılır


"""
