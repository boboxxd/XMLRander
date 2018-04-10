#!/usr/bin/python
# -*- coding: UTF-8 -*-

import os
import shutil
import glob
from xml.dom.minidom import parse
import xml.dom.minidom


def moveimage(image,alarmtype):
	isExists = os.path.exists(alarmtype)
	if not isExists:
		os.makedirs(alarmtype)
	else:
		print "moving " ,image ," to ",alarmtype
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
	for file in  glob.glob(r"./*.xml"):
		lt=Parsexml(file)
		print num,':',lt
		num=num+1

