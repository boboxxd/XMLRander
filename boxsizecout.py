#!/usr/local/bin/python3
# -*- coding: UTF-8 -*-

#!@Time   : 2018/4/12 上午10:40
#!@Author : xudongxu
#!@File   : boxsizecout.py

from xml.dom.minidom import parse
import xml.dom.minidom
import argparse

def readfile(filename):
	file = open(filename)
	L=(line.strip().replace('.jpg','.xml') for line in file)
	return L

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
			rect = n['rect']
			rectsize=abs((float(rect[2])-float(rect[0]))*(float(rect[3])-float(rect[1])))
			output.append(float(rectsize/imagesize))


def compare(value,output):
    step=0.05
    max=0.05
    while True:
        if value<max*max:
            key='%.2f*%.2f'%(max,max)
            if key not in output.keys():
                output[key]=0
            output[key]+=1
            break
        else:
            max=max+step
            continue



def count(input):
    rectdict={}
    tool=[]
    step=0.05
    rectdict['0.05*0.05']=0
    for n in input:
        maxpoint = 0.05 * 0.05
        compare(n,rectdict)
    return (rectdict)


def counttypes(input,output):
    for tp in input['objects']:
        for obj in tp:
            if obj['type'] not in output.keys():
                output[obj['type']]=1
            else:
                output[obj['type']]+=1





if (__name__ == "__main__"):

    parser = argparse.ArgumentParser()
    parser.add_argument('-f', '--file', help='imagelist file')
    args = parser.parse_args()
    txtfile = args.file

    output = []
    sum=0
    L=readfile(txtfile)

    typesout={}
    for n in L:
        try:
            result=Parsexml(n)
            sum+=1
            print('%d: Reading %s' %(sum,n))
            counttypes(result,typesout)
            rectslist(result,output)
        except Exception as e:
            pass
    #print (output)
    fin=count(output)

    print('--------------------------目标物大小统计------------------------------')
    print('-----------------------------统计结果--------------------------------')
    for i in typesout.keys():
        print(i,'---',typesout[i])
    print('--------------------------------------------------------------------')
    print('-----------------------------统计结果--------------------------------')

    print('--------------------------目标物大小统计------------------------------')
    print('-----------------------------统计结果--------------------------------')
    for i in fin.keys():
        print('<',i,'---',fin[i])
    print('--------------------------------------------------------------------')
    print('-----------------------------统计结果--------------------------------')