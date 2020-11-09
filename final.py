# encoding:utf-8
"""
---Fonksiyon Tanımları---

cueStickDetector: Istakayı tanımlar ve izlerini kaydeder.
drawBorders: Bilardo masasındaki; iç havuz, dış havuz ve topun yarı çapı kadar daha içeride olmak üzere 3 adet çerçeve çizer. Masadaki koordinat noktalarını belirtir.

"""

# -- Libraries -- #
import numpy as np
import cv2
import argparse

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

		#self.lower_blue = np.array([99,137,170])
		#self.upper_blue = np.array([180,219,250])

		self.lower_blue = np.array([84,0,0])
		self.upper_blue = np.array([180,140,255])

		# Rectangle Paramaters
		self.rectangle_flag = 0
		self.x , self.y, self.w, self.h = 0,0,0,0
		self.RectCol=(255,255,100)

		# Coordinate Points Parameters
		self.PointCol = (0,0,255)
		self.cPointsFlag = 0

		# Pool Edge Width
		self.pew = 13

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

		print("Class initialized...")

	def cueStickDetector(self):
		total_lines = []
		while(1):
			ret, img = cap.read()
			# (1) create a copy of the original:


			hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

			# Threshold the HSV image to get only blue colors
			mask = cv2.inRange(hsv, self.lower_blue, self.upper_blue)

			# Bitwise-AND mask and original image
			res = cv2.bitwise_and(img,img, mask= mask)

			# Find largest contour surrounds the blue field(pool)
			contours, hierarchy = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
			if len(contours) != 0:
				cnt = max(contours, key = cv2.contourArea)
				x,y,w,h = cv2.boundingRect(cnt)

			# Crops the original image to pool sized image
			img2 = img[y+self.FraC:y+h-self.FraC,x+self.FraC:x+w-self.FraC,:]
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
					print("counter",counter)
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

			img = self.drawBorders(img)
			cv2.imshow('image2', img2)

			cv2.imshow('image', img)

			k = cv2.waitKey(30) & 0xff
			if k == 27:
			    break

	def drawBorders(self,img_crop):
		hsv = cv2.cvtColor(img_crop, cv2.COLOR_BGR2HSV)
		# Threshold the HSV image to get only blue colors
		mask = cv2.inRange(hsv, self.lower_blue, self.upper_blue)

		# Bitwise-AND mask and original image
		res = cv2.bitwise_and(img_crop,img_crop, mask= mask)

		contours, hierarchy = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
		if len(contours) != 0:
		    cnt = max(contours, key = cv2.contourArea)
		    # To detect only rectangles in first frame (it prevents rectangles to shake)
		    if self.rectangle_flag != 1:
		        self.x,self.y,self.w,self.h = cv2.boundingRect(cnt)

		cv2.rectangle(img_crop,(self.x,self.y),(self.x+self.w,self.y+self.h)  ,self.RectCol,1)
		cv2.rectangle(img_crop,(self.x+self.pew,self.y+self.pew),(self.x+self.w-self.pew,self.y+self.h-self.pew)  ,self.RectCol,1)
		cv2.rectangle(img_crop,(self.x+self.pew+self.br,self.y+self.pew+self.br),(self.x+self.w-self.pew-self.br,self.y+self.h-self.pew-self.br)  ,self.RectCol,1)
		#cv2.rectangle(img_crop,(self.x+self.br,self.y+self.br),(self.x+self.w-self.br,self.y+self.h-self.br)  ,self.RectCol,1)

		#Drawing Coordinate Points
		if self.cPointsFlag != 1:
			for i in range(self.w):
				if i%self.cpi == 0:
				    cv2.circle(img_crop, (int(self.x+self.pew + i),self.y-self.pew), 4, self.PointCol, -1)

			for i in range(self.h):
			    if i%self.cpi == 0:
			        cv2.circle(img_crop, (self.x-self.pew,int(self.y+self.pew + i)), 4, self.PointCol, -1)

		self.cPointsFlag = 1
		self.rectangle_flag = 1

		return img_crop

	def ballDetector(self,img):
		img2 = img.copy()
		try:
			img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
			img = cv2.medianBlur(img,5)
			cimg = cv2.cvtColor(img,cv2.COLOR_GRAY2BGR).copy()
			circles = cv2.HoughCircles(img,cv2.HOUGH_GRADIENT,1,20,
			                            param1=50,param2=20,minRadius=9,maxRadius=15)
			circles = np.uint16(np.around(circles))
			for i in circles[0,:]:
			    # draw the outer circle
			    cv2.circle(img2,(i[0],i[1]),i[2],(0,255,0),2)
			    # draw the center of the circle
			    cv2.circle(img2,(i[0],i[1]),2,(0,0,255),3)
			return img2
		except:
			return img2



def main():
    bill = Billiards()
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

bu günlük 2 saat

15:30

"""
