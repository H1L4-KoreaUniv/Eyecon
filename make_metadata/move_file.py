import os
import shutil
import re

path_0 = 'C:/Users/sodaus/Desktop/data/ver3_0821_0235am/eyelm_img/0/'
path_1 = 'C:/Users/sodaus/Desktop/data/ver3_0821_0235am/eyelm_img/1/'

left_0 = 'C:/Users/sodaus/Desktop/data/ver3_0821_0235am/eyelm_left_img/0'
left_1 = 'C:/Users/sodaus/Desktop/data/ver3_0821_0235am/eyelm_left_img/1'

right_0 = 'C:/Users/sodaus/Desktop/data/ver3_0821_0235am/eyelm_right_img/0'
right_1 = 'C:/Users/sodaus/Desktop/data/ver3_0821_0235am/eyelm_right_img/1'

filelist_0 = os.listdir(path_0)
filelist_1 = os.listdir(path_1)

[shutil.move(path_0 + name, left_0) 
 if 'left' in name else shutil.move(path_0 + name, right_0)
 for name in filelist_0]

[shutil.move(path_1 + name, left_1) 
 if 'left' in name else shutil.move(path_1 + name, right_1)
 for name in filelist_1]