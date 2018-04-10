#!/usr/bin/python3
# -*- coding: UTF-8 -*-

from PIL import Image
import argparse
import glob


def getimagesize(filename):
	im= Image.open(filename)
	return im.size

if __name__=='__main__':
	sets=set()
	result={}
	flag=True
	parser = argparse.ArgumentParser()
	parser.add_argument('-d', '--path', help='floder of images')
	args=parser.parse_args()
	path=args.path
	L= (file for file in glob.glob(path+'/'+'*.jpg'))
	while flag:
		try:
			name=next(L)
			pixmsg={}
			pixmsg['name']=name
			pixmsg['size']=getimagesize(name)
			if pixmsg['size'] not in sets:
				sets.add(pixmsg['size'])
				result[pixmsg['size']]=1
			else:
				result[pixmsg['size']]+=1
		except Exception as e:
			flag=False

	for key in result:
		print (key,'---',result[key])

			





