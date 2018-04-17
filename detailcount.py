#!/usr/local/bin/python3
# -*- coding: UTF-8 -*-

#!@Time   : 2018/4/12 上午10:40
#!@Author : xudongxu
#!@File   : boxsizecout.py

from xml.dom.minidom import parse
import xml.dom.minidom
import argparse
import glob

# def readfile(filename):
# 	file = open(filename)
# 	L=(line.split('.')[0]+'.xml' for line in file)
# 	return L

def Parsexml(xmlname):
	result={}
	DOMTree = xml.dom.minidom.parse(xmlname)
	root = DOMTree.documentElement
	jpgname = root.getElementsByTagName("filename")[0].childNodes[0].data
	result['filename']=jpgname
	width=root.getElementsByTagName("width")[0].childNodes[0].data
	height = root.getElementsByTagName("height")[0].childNodes[0].data
	size=[width,height]
	result['size']=size
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

def rectslist(result,output):
	imagesize=float(result['size'][0])*float(result['size'][1])
	temp=result['objects']
	for L in temp:
		for n in L:
			objtype=n['type']
			rect=n['rect']
			rectsize=abs((float(rect[2])-float(rect[0]))*(float(rect[3])-float(rect[1])))
			if objtype not in output.keys():
				output[objtype]=[]
				#print('>>>>>>>>',rectsize,imagesize)
				output[objtype].append(float(rectsize/imagesize))
				#print('>>>>>>>',float(rectsize/imagesize))
			else:
				#print('>>>>>>>>', rectsize, imagesize)
				#print('>>>>>>>', float(rectsize / imagesize))
				output[objtype].append(float(rectsize/imagesize))

def compare(value,output,max,step):
	# step = 0.01
	# max = 0.01
	while True:
		if value <= max:
			if max-step<0:
				left=0
			else:
				left=max-step
			key = '(%.2f,%.2f]' % (left, max)
			if key not in output.keys():
				output[key] = 0
			output[key] += 1
			break
		else:
			max = max + step
			continue



def count(input,max,step):
	rectdict = {}#{'daodianxian':{'05*0.5':2,'1.0*1.0':2}}
	for i in input.keys():
		if i not in rectdict:
			rectdict[i]={}
		for n in input[i]:
			compare(n, rectdict[i],max,step)
	return (rectdict)




if (__name__ == "__main__"):
	parser = argparse.ArgumentParser()
	parser.add_argument('-d', '--filedir', help='image dir')
	args = parser.parse_args()
	xmldir = args.filedir

	output = {}
	sum=0
	#L=readfile(txtfile)
	L=(file for file in glob.glob(xmldir+'/*.xml'))
	typesout={}
	typeboxs = {}  # {'type':jueyuanzi,'boxsize':[0.0002987816519154581, 1.2518555665863876e-06, 0.0002987816519154581]}
	for n in L:
		try:
			result=Parsexml(n)
			sum+=1
			print('%d: Reading %s' %(sum,n))
			rectslist(result,typeboxs)
		except Exception as e:
			pass
	print('--------------------------目标物大小统计------------------------------')
	print('-----------------------------统计结果--------------------------------')
	steplist=[0.01,0.02,0.03,0.04,0.05,0.1]
	for step in steplist:
		fin=count(typeboxs,0.05,step)

		print('step=%.2f'%step)
		for i in fin.keys():
			print('===%s===='%i)
			for n in fin[i].keys():
				print(n, '---', fin[i][n])
		print('<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<')
print('-----------------------------统计结束--------------------------------')

