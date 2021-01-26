import numpy as np
import pandas as pd

data_w_x = pd.read_csv('white_center.csv',index_col=0)
data_w_y = pd.read_csv('white_center.csv',index_col=1)
data_y =  np.loadtxt('yellow_center.csv', delimiter=',')
data_r =  np.loadtxt('red_center.csv', delimiter=',')

data_w_x = np.array(data_w_x)
data_w_y = np.array(data_w_y)

pol = np.polyfit(data_w_x,data_w_y,2,rcond=None, full=False, w=None, cov=False)

