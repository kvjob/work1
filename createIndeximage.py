import os
import ipdb
import numpy as np
import cv2
from matplotlib import pyplot as plt
import ast
from sys import exit
import ipdb
from difflib import SequenceMatcher

def similar(a, b):
# this function is designed for identifying the similarity between various length strings
'''
eg strings
a = 'he is a man'
b = 'man'
The function will be true for this input
 
'''
	if len(b)>len(a):
		base = a
		for i in range(0, len(b)-len(a)):
			if SequenceMatcher(None, base, b[i:i+len(a)]).ratio()>0.8:
				return True
				break
	elif len(a)>len(b):
		base = b
		for i in range(0, len(a)-len(b)):
			if SequenceMatcher(None, base, a[i:i+len(b)]).ratio()>0.8:
				return True
				break
	else:
		if SequenceMatcher(None, a, b).ratio()>0.8:
			return True
			
		
	return False

# all available images
imgdir = '../trainSet1/img/'

# annotation of each text region cordinates and its text value
annotation1 = '../task1_train/'

# annotation of key information such as date, company, address and total amount
annotation2 = '../task2_train/'

# output folders
output_ind = './ind/' #to save the index images 
output_ind1 = './viz/' # to save the visualization image
output_blend = '/home/jobinkv/Documents/r1/c1/mergeVis/'

# function for checking text in each region is belongs to any key information 
# if the text is in any key information the fuction return its key 
def getKey(dictionary, val):
	key_return='' # default key return
	flag = 0 #flag 1--> if it have any key else 0
	i = 0
	for key, value in dictionary.items(): 
		# trim the comparing string, remove space and .
		imp_val  = val.replace(' ','').replace('.','').replace(',','') 
		dic_val  = value.replace(' ','').replace('.','').replace(',','')
		if dic_val=='' or imp_val=='':# skip if any text is null
			continue 
		i = i+1
		'''
		'''
		if len(val)>2: # assume all valid region have minimum 2 characters
    			if imp_val in dic_val:# check the block text in dictionary
				key_return = key
				flag=1
        			return key_return,i
    			elif dic_val in imp_val: # check dictionary text in block text
				key_return = key
				flag=1
        			return key_return,i
			elif similar(dic_val, imp_val): # similarity between various length strings 
				key_return = key
				flag=1
        			return key_return,i
				
	if flag==0:
		return 'background',0

# get a list of all images in the image folder
fileList = os.listdir(imgdir)

# iterate through each image
for item in fileList:
	# create annotation file name
	txtName = item.replace('.jpg','.txt')
	# file have position cordinates 
	filepath = annotation1+txtName
	# file have dictonary
	seconAnnotation = annotation2+txtName
	# it will create the gt(ind) file which have both the annotation
	if  (os.path.exists(seconAnnotation) and os.path.exists(filepath) and os.path.exists(imgdir+item)):
		print item
		'''
		if item=='X51006414599.jpg':
			print 'got him'
		else:
			continue
		'''
		#read the dictonary
		secAnotation_dict = eval(open(seconAnnotation).read())
		#read the position file, each line contains 8py cordinates and its text value 	
		lines = [line.rstrip('\n') for line in open(filepath)]
		# read the image file
		im = cv2.imread(imgdir+item)[:, :, ::-1]
		# intitialize ind and viz output files
		ind = np.zeros((im.shape[0],im.shape[1]), np.uint8)
		viz = np.zeros((im.shape[0],im.shape[1],3), np.uint8)
		# set the output path
		outPath = output_ind+item.replace('.jpg','.png')
		outPath1 = output_ind1+item.replace('.jpg','.png')
		outPath2 = output_blend+item.replace('.jpg','.png')
		# trad each line in the position annotation
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
			# the text value it is possible to occure
			txtVal = ''
			for i in range(8,len(vals)):
				txtVal = txtVal+vals[i]
			# check the text value in in any label
			inbel,ids = getKey(secAnotation_dict,txtVal)
			if ids==0: # back ground
				cv2.fillPoly(viz, box.astype(np.int32).reshape((1, -1, 2)),(0, 0, 0))
			if ids==1: # date 
				cv2.fillPoly(viz, box.astype(np.int32).reshape((1, -1, 2)),(0, 0, 255))
			if ids==2: # company
				cv2.fillPoly(viz, box.astype(np.int32).reshape((1, -1, 2)),(0, 255, 0))
			if ids==3: # total
				cv2.fillPoly(viz, box.astype(np.int32).reshape((1, -1, 2)),(255, 0, 0))
			if ids==4: # Address
				cv2.fillPoly(viz, box.astype(np.int32).reshape((1, -1, 2)),(255, 0, 255))
			# creating the index image
			cv2.fillPoly(ind, box.astype(np.int32).reshape((1, -1, 2)),(ids))
		# [blend_images]
		alpha = 0.5
		beta = (1.0 - alpha)
		blended = cv2.addWeighted(viz, alpha, im, beta, 0.0)
		# write both the images
		cv2.imwrite(outPath,ind);	
		cv2.imwrite(outPath1,viz);	
		cv2.imwrite(outPath2,blended);	
       		view=0
		# to debugg
       		if view==1:
       			# show our images
        	        plt.figure("image")
       		        #plt.imshow(imutils.resize(orig, height = 300))
      		        plt.imshow(blended)
      	        	plt.show()
                	ipdb.set_trace()
