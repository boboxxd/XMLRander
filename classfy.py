#!/usr/local/bin/python3
# -*- coding: UTF-8 -*-

import os
import shutil
import glob
import argparse
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

if (__name__=="__main__"):
	num = 0
	parser = argparse.ArgumentParser()
	parser.add_argument('-f', '--imagelist', help='imageslist file')
	args=parser.parse_args()
	imagelist=args.imagelist
	path = os.path.dirname(imagelist)
	#for file in  glob.glob(path+"*.xml"):
	for file in readfile(imagelist):
		print(file)
		try:
			lt=Parsexml(file)
			print(num, ':', lt)
			moveimage(lt['JpgName'],path+'/'+lt['AlarmObjects'][0])
			num=num+1
		except Exception as e:
			pass


