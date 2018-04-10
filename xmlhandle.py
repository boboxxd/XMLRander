#!/usr/bin/python3
# -*- coding: UTF-8 -*-

import os
import shutil
import glob
from xml.dom.minidom import parse
import xml.dom.minidom
import sqlite3

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


#解析输出文件result.txt
class Parsetxt:
    def __init__(self, txtname):
        self.txtname = txtname
        self.textpath = os.path.dirname(txtname)
        self.dbname=self.textpath+'/result.db'
        if  os.path.exists(self.dbname):
        	os.remove(self.dbname)
        self.initdb()

    def initdb(self):
    	self.conn = sqlite3.connect(self.dbname)
    	print ('Opened database successfully')
    	self.c = self.conn.cursor()
    	self.c.execute('''CREATE TABLE results
			(ID INT PRIMARY KEY     NOT NULL,
			NAME           TEXT    NOT NULL,
			TYPE           TEXT     NOT NULL,
			SCORE        REAL,
			XMIN         REAL,
			YMIN        REAL,
			XMAX         REAL,
			YMAX        REAL);''')
    	print ('Table created successfully')
    	self.conn.commit()
    	file = open(self.txtname)
    	for line in file:
    		lists=line.strip().split(',')
    		sql="INSERT INTO results(ID,NAME,TYPE,SCORE,XMIN,YMIN,XMAX,YMAX) VALUES (?,?,?,?,?,?,?,?)"
    		para=(lists[0],lists[1],lists[2],lists[3],lists[4],lists[5],lists[6],lists[7])
    		self.c.execute(sql,para)
    	self.conn.commit()
    	self.conn.close()
    	file.close()

    def getmsg(self,jpgpath):
    	lists=[]
    	rows=()
    	jpgname=os.path.basename(jpgpath)
    	conn = sqlite3.connect(self.dbname)
    	c = conn.cursor()
    	sql='select TYPE,XMIN,YMIN,XMAX,YMAX from results where NAME =?'
    	query=c.execute(sql,(jpgname,))
    	for row in query:
    		rows=(row[0],row[1],row[2],row[3],row[4])
    		lists.append(rows)
    	conn.commit()
    	conn.close()
    	return lists



if (__name__=="__main__"):
	#print(Parsexml('test.xml'))
	txtpraser=Parsetxt('image/result.txt')
	lists=txtpraser.getmsg('image/test.jpg')
	print(lists)




