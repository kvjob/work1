import os
import ipdb
import numpy as np
import cv2
from matplotlib import pyplot as plt
import ast
from sys import exit
import ipdb


imgdir = './img/'
annotation1 = './task1_train/'
annotation2 = './task2_train/'
output_ind = './ind/'
output_ind1 = './viz/'

def getKey(dictionary, val):
	key_return=''
	flag = 0
	i = 0
	for key, value in dictionary.items():    # for name, age in dictionary.iteritems():  (for Python 2.x)
		i = i+1
    		if key in ['date','total']:
			ipdb.set_trace()
    			#if val in value:
    			if val == value:
				key_return = key
				flag=1
        			return key_return,i
    		if key in ['company','address']:
    			if val in value:
				key_return = key
				flag=1
        			return key_return,i
	if flag==0:
		return 'background',0

fileList = os.listdir(imgdir)

for item in fileList:
	txtName = item.replace('.jpg','.txt')
	filepath = annotation1+txtName
	seconAnnotation = annotation2+txtName
	if not (os.path.exists(seconAnnotation) and os.path.exists(filepath) and os.path.exists('./img/'+item)):
		print item
		continue
	secAnotation_dict = eval(open(seconAnnotation).read())
	#print open(seconAnnotation).read()	
	lines = [line.rstrip('\n') for line in open(filepath)]
	im = cv2.imread('./img/'+item)[:, :, ::-1]
	ind = np.zeros((im.shape[0],im.shape[1]), np.uint8)
	viz = np.zeros((im.shape[0],im.shape[1],3), np.uint8)
	#viz = np.zeros(im.shape, np.uint8)
	outPath = output_ind+item.replace('.jpg','.png')
	outPath1 = output_ind1+item.replace('.jpg','.png')
	for line in lines:
		box = np.zeros((4, 2))
		vals = line.split(',')
		box[0, 0]= vals[0]
		box[0, 1]= vals[1]
		box[1, 0]= vals[2]
		box[1, 1]= vals[3]
		box[2, 0]= vals[4]
		box[2, 1]= vals[5]
		box[3, 0]= vals[6]
		box[3, 1]= vals[7]
		txtVal = vals[8]
		inbel,ids = getKey(secAnotation_dict,txtVal)
		#pts = box.astype(np.int32).reshape((1, -1, 2))[0]
		if ids==0:
			cv2.fillPoly(viz, box.astype(np.int32).reshape((1, -1, 2)),(0, 0, 0))
		if ids==1:
			cv2.fillPoly(viz, box.astype(np.int32).reshape((1, -1, 2)),(0, 0, 255))
		if ids==2:
			cv2.fillPoly(viz, box.astype(np.int32).reshape((1, -1, 2)),(0, 255, 0))
		if ids==3:
			cv2.fillPoly(viz, box.astype(np.int32).reshape((1, -1, 2)),(255, 0, 0))
		if ids==4:
			cv2.fillPoly(viz, box.astype(np.int32).reshape((1, -1, 2)),(255, 0, 255))
		cv2.fillPoly(ind, box.astype(np.int32).reshape((1, -1, 2)),(ids))
		#print  txtVal,'\t \t \t \t \t \t \t', inbel,ids
	cv2.imwrite(outPath,ind);	
	cv2.imwrite(outPath1,viz);	
        view=0
        if view==1:
                # show our images
                plt.figure("image")
                #plt.imshow(imutils.resize(orig, height = 300))
                plt.imshow(ind)
                plt.show()
                ipdb.set_trace()
