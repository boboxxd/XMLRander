#!/usr/local/bin/python3
# -*- coding: UTF-8 -*-

import os
import shutil
import glob
import argparse
import sys
from xml.dom.minidom import parse
import xml.dom.minidom


def readfile(filename):
	file = open(filename)
	L=(line.strip().replace('.jpg','.xml') for line in file)
	return L

def moveimage(image,alarmtype):
	isExists = os.path.exists(alarmtype)
	if not isExists:
		os.makedirs(alarmtype)
	else:
		print ("------> moving " ,image ," to ",alarmtype)
		#shutil.move(image,alarmtype)

#解析xml
def Parsexml(xmlname):
	File={}
	Objects=[]
	DOMTree = xml.dom.minidom.parse(xmlname)
	collection = DOMTree.documentElement
	jpgname=collection.getElementsByTagName("filename")[0].childNodes[0].data
	File['JpgName']=jpgname

	objects = collection.getElementsByTagName("object")
	for alarmobject in objects:
		type = alarmobject.getElementsByTagName('name')[0]
		Objects.append(type.childNodes[0].data)
	File['AlarmObjects']=Objects
	return File


#in: type,path
#out: filelist

def select(type,path):
	filelist=[]
	output = open(path+'/'+type+'.txt', 'w')
	#output.truncate()
	for file in glob.glob(path+'/*.xml'):
		try:
			lt = Parsexml(file)
			for obs in lt['AlarmObjects']:
				if type == obs:
					jpgname=lt['JpgName']
					print(jpgname.split('.')[0])
					output.write(jpgname.split('.')[0]+'\n')
			#
		except Exception as e:
			#output.close()
			pass
	output.close()



if (__name__=="__main__"):
	# num = 0
	# parser = argparse.ArgumentParser()
	# #读取txt,并分类
	# parser.add_argument('-f', '--imagelist', help='imageslist file')
	# args=parser.parse_args()
	# imagelist=args.imagelist
    #
	# path = os.path.dirname(imagelist)
	# #for file in  glob.glob(path+"*.xml"):
	# for file in readfile(imagelist):
	# 	print(file)
	# 	try:
	# 		lt=Parsexml(file)
	# 		print(num, ':', lt)
	# 		moveimage(lt['JpgName'],path+'/'+lt['AlarmObjects'][0])
	# 		num=num+1
	# 	except Exception as e:
	# 		pass

	if len(sys.argv)!=3:
		print('''usage: ./classfy  type  path ''')
	try:
		select(sys.argv[1],sys.argv[2])
	except  Exception as e:
		pass



