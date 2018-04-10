#!/usr/bin/python3
# -*- coding: UTF-8 -*-

import os
import shutil
import glob
from xml.dom.minidom import parse
import xml.dom.minidom

#读取xml，保存到字典中
def Parsexml(xmlname):
	result={}
	DOMTree = xml.dom.minidom.parse(xmlname)
	root = DOMTree.documentElement
	jpgname = root.getElementsByTagName("filename")[0].childNodes[0].data
	result['filename']=jpgname


	alarmobjects=[]
	objectsnodes = root.getElementsByTagName("object")
	for onode in objectsnodes:
		alarmobject = {}
		type = onode.getElementsByTagName('name')[0].childNodes[0].data
		alarmobject['type']=type
		boxs = onode.getElementsByTagName("bndbox")
		for box in boxs:
			xmin=box.getElementsByTagName('xmin')[0].childNodes[0].data
			ymin = box.getElementsByTagName('ymin')[0].childNodes[0].data
			xmax = box.getElementsByTagName('xmax')[0].childNodes[0].data
			ymax = box.getElementsByTagName('ymax')[0].childNodes[0].data
			alarmobject['rect']=[xmin,ymin,xmax,ymax]
			alarmobjects.append(alarmobject)
	result['objects']=[alarmobjects]
	return result

if (__name__=="__main__"):
	print(Parsexml('test.xml'))




