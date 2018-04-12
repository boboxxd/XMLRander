#!/usr/local/bin/python3
# -*- coding: UTF-8 -*-

from PIL import Image
import argparse
import glob


def getimagesize(filename):
	im= Image.open(filename)
	return im.size

def readfile(filename):
	file = open(filename)
	L=(line.strip() for line in file)
	return L

if __name__=='__main__':
	index=0
	sets=set()
	result={}
	flag=True
	parser = argparse.ArgumentParser()
	parser.add_argument('-d', '--path', help='floder of images')
	parser.add_argument('-f','--file',help='imagelist file')
	args=parser.parse_args()

	path=args.path
	txtfile=args.file

	if path:
		L= (file for file in glob.glob(path+'/'+'*.jpg'))
	if txtfile:
		L=readfile(txtfile)

	while flag:
		try:
			name=next(L)
			index+=1
			pixmsg={}
			pixmsg['name']=name
			pixmsg['size']=getimagesize(name)
			print(pixmsg['name'])
			print(pixmsg['size'])
			if pixmsg['size'] not in sets:
				sets.add(pixmsg['size'])
				result[pixmsg['size']]=1
			else:
				result[pixmsg['size']]+=1
		except Exception as e:
			flag=False
		print('%d: get image %s size:'%(index,name),pixmsg['size'])

	print('--------------------------------------------------------------------')
	print('-----------------------------统计结果--------------------------------')

	for key in result:
		print (key,'---',result[key])

	print('----------------------------统计结束---------------------------------')
	print('--------------------------------------------------------------------')





