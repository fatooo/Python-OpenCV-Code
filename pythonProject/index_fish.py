import numpy as np
import cv2
import time

map_x = np.loadtxt('map_x.csv', delimiter=',')
map_y = np.loadtxt('map_y.csv', delimiter=',')
map_x = np.rint(map_x)
map_y = np.rint(map_y)

map_x_cons = np.zeros(shape=(1080,1920))
map_y_cons = np.zeros(shape=(1080,1920))

for i in range(1080):
    map_x_cons[i][:] = range(1920)

for i in range(1080):
    map_y_cons[i][:] = i

map_x = map_x + map_x_cons
map_y = map_y + map_y_cons

#np.savetxt("C:\\Users\\fatma\\PycharmProjects\\pythonProject\\map_x_idx.txt", map_x, delimiter=",",fmt='%d')
#np.savetxt("C:\\Users\\fatma\\PycharmProjects\\pythonProject\\map_y_idx.txt", map_y, delimiter=",",fmt='%d')


coords = np.zeros(shape=(1080*1920,2),dtype=int)
coords_T = np.zeros(shape=(2,1080*1920),dtype=int)
for i in range(1080):
    for k in range(1920):
        coords[i*1920+k][:]=int(map_y[i][k]),int(map_x[i][k])
coords_T = coords.T

img = cv2.imread('C:\\Users\\fatma\\Desktop\\Bilardo\\map\\salon5.jpg')
t_rasa = np.zeros_like(img)
start_time = time.time()

t_rasa = (img[tuple(coords_T)]).reshape((1080, 1920,3))

print("--- %s seconds ---" % (time.time() - start_time))
print(t_rasa.shape)
cv2.imshow('dene',t_rasa),cv2.waitKey(0),cv2.destroyAllWindows()

